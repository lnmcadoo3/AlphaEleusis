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

#This will hold the representation of all of the cards, 
#   both legal and illegal, that have been played
BOARD = []
RULE = None
HYPOTHESIS = None
HAND = []

def pick_card():
    """
    Helper function that picks a card from the HAND, for Phase I, the hand
    includes all possible cards
    
    TODO: Phase II gamification
    """
    for card in HAND:
        # if card is illegal under the hypothesis, play it
        if HYPOTHESIS and not HYPOTHESIS.evaluate(card):
            # TODO: phase II should remove the card from the hand
            return card
        
    return pick_card_at_random()

def pick_card_at_random():
    """
    Helper function that returns a random card from the hand
    """
    # TODO: Phase II should remove the played card from the hand
    return random.choice(HAND)

def deal_hand():
    """
    Deals a hand to the player, if this is phase one, this is every possible card
    """
    # TODO: Phase II
    for suit in ["C", "D", "H", "S"]:
        for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            HAND.append(value + suit)

def create_datum(card, truth):
    """
    Input: The last card played
    Output: A datum for the training set, based on the previous 2 cards

    Requires that 2 legal cards have been played
    """
    b = boardState()
    prev = b[-1][0]
    prev2 = b[-2][0]

    cards = [prev2, prev, card]

    # we need suit, parity, color...
    individuals = [suit, even, color, is_royal]

    features = [x(y) for y in cards for x in individuals]
    #print(features)

    # unfortunately we need features for comparing values (for each card) 
    #   to the numbers 1 to 13, to encompass numerical differences
    # this makes the feature list gigantic
    features += [x(str(y[:-1]), str(z)) for y in cards for z in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] for x in [greater, equal]]

    # compare the deck values of the cards to each other
    features += ([x(card, y) for y in [prev, prev2] for x in [greater, equal]] + [x(prev, prev2) for x in [greater, equal]])

    #TODO: add anything else here that could possibly be a predicate that we split on

    # include the classification
    features.append(truth)

    #print(card, features, len(features))
    return tuple(features)

def retrain(training_data):
    """
    Input: Training data
    Output: A decision tree representing our agent's hypothesis
    """
    return None


def scientist():
    """
    Input: None
    Output: Returns the <rule-expression> the player has found
    
    Also updates the board state
    Requires that 2 legal cards have been played
    """
    cards_played = 0
    guesses_correct = 0

    # this should be the running list of training data (so that we don't have to recompute)
    training_data = []

    dt = DecisionTree()

    while(cards_played < 200):
        cards_played += 1

        # somehow choose a card
        card = pick_card()

        print("CARD", card)

        # our guess vs. actual truth
        truth = play(card)
        datum = create_datum(card, truth)

        #This should be a fixed constant
        attrs = [str(i) for i in range(len(datum))]

        if(cards_played > 1):
            guess = dt.predict(attrs, [datum])[0]
            if(guess == "Null"):
                guess = False
        else:
            guess = False

        print("GUESS", guess)

        # TODO: Add the card (and its precessors to the training data set)
        training_data.append(datum)

        # if we are incorrect
        if(guess != truth or cards_played == 1):
            #print("BUILDING TREE")
            dt.build_tree(training_data, attrs[-1], attrs)
            print(dt.tree)
            guesses_correct = 0
        # if we guessed right
        else:
            guesses_correct += 1

        if(cards_played > 1):
            print(dt.tree, guesses_correct)

        # quitting criterion (subject to change)
        if(cards_played > 20 and guesses_correct > 10):
            return HYPOTHESIS

    return HYPOTHESIS

def score():
    """
    Input: None
    Output: Returns the score for the most recent round. (Low is better!)
    Calculate by adding points as follows: +1 for every successful play over 20
    and under 200; +2 for every failed play; + 15 for a rule that is not
    equivalent to the correct rule; +30 for a rule that does not describe all
    cards on the board.
    """
    board = boardState()
    legal_plays = {}
    illegal_plays = {}
    card_num = 1
    for (legal, illegals) in board:
        if(len(illegals) != 0):
            for illegal in illegals:
                illegal_plays[card_num] = illegal
                card_num += 1
        legal_plays[card_num] = legal
        card_num += 1

    #Scoring for the legal or illegal plays
    score = len([x for x in legal_plays.keys() if x >= 20]) + 2*len([y for y in illegal_plays.keys() if y >= 20])

    #Score the rule etc.

    return score


def play(card):
    """
    Input: <card>
    Output: True if the play was legal, False otherwise
    """
    #Grab the 2 previous cards:
    b = boardState()
    previous2 = None
    previous2 = None
    if(len(b) >= 1):
        previous = b[-1][0]
    if(len(b) >= 2):
        previous2 = b[-2][0]
    legal = RULE.evaluate((previous2, previous, card))

    #Should be the only place that BOARD is updated
    if(legal):
        BOARD.append((card, []))
    else:
        BOARD[-1][1].append(card)

    return legal

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

def play_game(rule, legals):
    """
    Input: A rule for a game, and the first 2 plays for that rule
    Output: The score for the scientist after playing with that rule
    """
    if(BOARD):
        BOARD = None
    if(RULE):
        RULE = None

    set_rule(rule)
    for i in legals:
        BOARD.append((i, []))

    print(scientist())
    print(score())



def main():
    print("Starting a new game of New Eleusis!")
    
    print("God is choosing a rule...")
    set_rule("equal(color(previous), color(current))")
    print("God chose the rule:")
    print(RULE)
    
    print("Dealing the player a hand...")
    deal_hand()
    print("Players hand is:")
    print(HAND)
    
    BOARD.append(("9D", []))
    BOARD.append(("8H", []))

    scientist()

    #next_card = pick_card_at_random()
    #next_card = pick_card()
    #print("Player is playing:")
    #print(next_card)
    
    #print("God says...")
    #print("Legal") if play(next_card) else print("Illegal")

    """
    play("6D")
    x = create_datum("6D", True)
    play("7C")
    y = create_datum("7C", False)
    play("8H")
    z = create_datum("8H", True)
    play("9S")
    x1 = create_datum("9S", False)
    play("5H")
    x2 = create_datum("5H", True)



    attrs = [str(i) for i in range(len(x))]

    dt = DecisionTree()
    dt.build_tree([x,y,z,x1,x2], attrs[-1], attrs)

    print(dt.predict(attrs, [z]))
    print(dt.tree)


    print(len(x))

    """

    #print(boardState())

    """
    rules = []
    rules.append(("equal(color(previous), color(current))", ("9D", "3H")))
    for (r, legal) in rules:
        play_game(r, legal)
    """

main()
