"""
ALPHA Eleusis
CMSC 671
Dr. Matuszek
 
Authors:
    Patrick Jenkins
    Leslie McAdoo
    Akshayvarun Subramanya
"""

from new_eleusis import *
from Decision_Tree import DecisionTree
import random

global game_ended


class Player(object):

    def __init__(self, cards):
        """
        Pretty self explanatory constructor
        """

        #These variables replace the global variables in Phase I
        self.BOARD = []   
        self.VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.SUITS = ["C", "D", "H", "S"]
        self.DECK = [x+y for x in self.VALUES for y in self.SUITS]


        #Helper variables for ATTRIBUTES
        cards_att = ["previous2", "previous", "current"]
        individuals_att = ["suit", "color", "even", "is_royal"]
        self.ATTRIBUTES = [x + "(" + str(y) + ")" for y in cards_att for x in individuals_att]
        self.ATTRIBUTES += [x + "(value(" + y + ")," + z + ")" for y in cards_att for z in self.VALUES for x in ["greater", "equal"]]
        self.ATTRIBUTES += [x + "(current" + "," + y + ")" for y in cards_att[:-1] for x in ["greater", "equal"]]
        self.ATTRIBUTES += [x + "(previous, previous2)" for x in ["greater", "equal"]]
        self.ATTRIBUTES += [x + "(value(current)" + ",value(" + y + ")" for y in cards_att[:-1] for x in ["greater", "equal"]]
        self.ATTRIBUTES += [x + "(value(previous), value(previous2))" for x in ["greater", "equal"]]
        self.ATTRIBUTES += ["Legal"]

        #To keep track of running score
        self.score = 0
        self.ended_game = False

        #This is for our rule
        self.hypothesis = DecisionTree()
        self.training_data = []

        #A boolean that will tell us if we need to update the tree
        self.rebuildTree = True

        #These are for our quitting criteria
        self.cards_played = []
        self.total_cards = 0
        self.guesses_correct = 0


        #Setup the initial boardstate
        for c in cards:
            self.update_card_to_board_state(c, True)

        #Setup our hand
        self.hand = [self.generate_random_card() for i in range(14)]


    """
    Helper function that picks a card from the HAND, for Phase I, the hand
    includes all possible cards
    
    TODO: Phase II gamification
    """
    def pick_card(self):
        return random.choice(self.hand)

    """
    Returns random card in the deck
    """
    def generate_random_card(self):
        return random.choice(self.VALUES) + random.choice(self.SUITS)

    """
    Takes in a card and whether or not it was legal, updating the board state

    We will also update our training data here, and decide whether or not we need to rebuild the
        decision tree

    TODO: find a way to update our score if we played the card?
    """
    def update_card_to_board_state(self, card, result):

        #Construct an element of the training data
        datum = self.create_datum(card)
        datum.append(result)
        datum = tuple(datum)

        self.training_data.append(datum)

        #Figure out what our rule says about this card
        guess = self.guess_legal(datum)

        #If we were wrong, we need to rebuild the tree
        if(guess != result):
            self.rebuildTree = True
            self.guesses_correct = 0
        #We were correct, and our tree is not proven wrong
        elif(guess == result and not self.rebuildTree):
            self.guesses_correct += 1

        #Now we can update the board state
        if(result):
            self.BOARD.append((card, []))
        else:
            self.BOARD[-1][1].append(card)

        #Increase our score (iff we played the card and it counts towards score)
        if(len(self.cards_played) > 20 and self.cards_played[-1] == self.total_cards):
            #if the card was legal
            if(result):
                self.score += 1
            else:
                self.score += 2

        #Increase the total number of cards that we've seen
        self.total_cards += 1

    """
    This takes in a card and returns the datum (without the classification, which will be added later)

    This assumes that card has *NOT* been added to the BOARD, i.e. we have not "played" card yet
    """
    def create_datum(self, card):
        prev2 = BOARD[-2][0]
        prev = BOARD[-1][0]

        cards = [prev2, prev, card]

        # we need suit, parity, color...
        individuals = [suit, color, even, is_royal]

        features = [x(y) for y in cards for x in individuals]

        # unfortunately we need features for comparing values (for each card) 
        #   to the numbers 1 to 13, to encompass numerical differences
        # this makes the feature list gigantic
        features += [x(str(y[:-1]), str(z)) for y in cards for z in self.VALUES for x in [greater, equal]]

        # compare the deck values of the cards to each other
        features += [x(card, y) for y in [prev2, prev] for x in [greater, equal]] + [x(prev, prev2) for x in [greater, equal]]

        #TODO: add anything else here that could possibly be a predicate that we split on
        features += [x(card[:-1], y[:-1]) for y in [prev2, prev] for x in [greater, equal]] 
        features += [x(prev[:-1], prev2[:-1]) for x in [greater, equal]]

        return features

    """
    Takes in a datum (create_datum(card)) and returns our hypothesis about whether the card is legal or not

    TODO: Verify that this works
    """
    def guess_legal(self, datum):

        guess = self.hypothesis.predict(self.ATTRIBUTES, [datum])[0]

        if(guess == "Null"):
            guess = False
        return guess

    """
    The core of the Player's decision making

    TODO: Update quitting criterion
    TODO: If we 
    """
    def scientist(self, game_ended):
        #quitting criteria
        quitting = (self.total_cards > 20) and (self.guesses_correct > 20)

        if(game_ended or quitting):
            #if we are ending the game
            if(not game_ended):
                self.ended_game = True
            return self.hypothesis.get_rule()
        else:
            #if we need to rebuild the tree, rebuild it
            if(len(self.training_data) > 0 and self.rebuildTree):
                #rebuild the tree
                self.hypothesis.build_tree(self.training_data, self.ATTRIBUTES[-1], self.ATTRIBUTES)

            #pick a card
            card = self.pick_card()

            #record what number card we played
            self.cards_played.append(self.total_cards)

            #play the card
            return card

    """
    This computes the score of the player
    """
    def score(self, rule):
        if(self.check_equivalence(rule)):
            self.score -= 75
        if(self.ended_game):
            self.score -= 25
        return self.score

    """
    This checks to see if the rule is equivalent to our hypothesis

    TODO: Maybe change this for vacuous stuff?
            -Maybe use (None, None, x) to see if the dealer could play x
                This would require a try catch because maybe None would cause it to fail
            -Maybe try and parse the rule to ignore prev2/prev for the first 2 cards etc?
                Like evaluate the parts of the rule that don't use prev/prev2

    """
    def check_equivalence(self, rule):
        for prev2 in self.DECK:
            for prev in self.DECK:
                for curr in self.DECK:
                    # should check for vacuous equivalence
                    if rule.evaluate((prev2, prev, curr)) != self.hypothesis.evaluate((prev2, prev, curr)):
                        return False
        return True

    """
    This is mostly a wrapper for scientist

    TODO: Make sure that this works with game_ended (being global and all)
    """
    def play(self):
        return scientist(self, game_ended)


def boardState():
    """
    Returns a list of plays so far as a sequential list of tuples,
    in order of play. Each tuple will contain a card played in the main
    sequence (that is, played successfully), then a list of all cards played
    unsuccessfully after it, which may be empty.
    """
    return BOARD

def set_rule(rule):
    """
    Input: <rule-expression>
    Output: None
    Set the current rule, using functions provided in new_eleusis.py
    """
    global RULE
    RULE = parse(rule)


def main():
    print("Starting a new game of New Eleusis!")
    
    print("God is choosing a rule...")
    set_rule("equal(color(previous), color(current))")
    
    '''
    set_rule("""and(
                        not(and(equal(color(previous), color(previous2)),
                                equal(color(previous), color(current))) ),
                        not(and(equal(value(previous), value(previous2)),
                                equal(value(previous), value(current))) ) )""")
    '''
    
    print("God chose the rule:")
    print(RULE)
    
    create_deck()
    print("Players hand is:")
    
    BOARD.append(("9D", []))
    BOARD.append(("8H", []))

    #rule = scientist()

    print(boardState())

    print("SCIENTIST'S GUESS:")
    #print(rule)
    
    
if __name__ == "__main__":
    main()
