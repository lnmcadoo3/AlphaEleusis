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
ATTRIBUTES = []

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
    global ATTRIBUTES

    b = boardState()
    if(truth):
        prev = b[-2][0]
        prev2 = b[-3][0]
    else:
        prev = b[-1][0]
        prev2 = b[-2][0]

    cards = [prev2, prev, card]
    cards_att = ["previous2", "previous", "current"]

    # we need suit, parity, color...
    individuals = [suit, color, even, is_royal]
    individuals_att = ["suit", "color", "even", "is_royal"]

    features = []
    ATTRIBUTES = []

    features += [x(y) for y in cards for x in individuals]
    ATTRIBUTES += [x + "(" + str(y) + ")" for y in cards_att for x in individuals_att]
    #print(ATTRIBUTES)
    #print(features)


    # unfortunately we need features for comparing values (for each card) 
    #   to the numbers 1 to 13, to encompass numerical differences
    # this makes the feature list gigantic
    features += [x(str(y[:-1]), str(z)) for y in cards for z in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] for x in [greater, equal]]
    ATTRIBUTES += [x + "(value(" + y + ")," + z + ")" for y in cards_att for z in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] for x in ["greater", "equal"]]

    # compare the deck values of the cards to each other
    features += ([x(card, y) for y in [prev2, prev] for x in [greater, equal]] + [x(prev, prev2) for x in [greater, equal]])
    ATTRIBUTES += ([x + "(current" + "," + y + ")" for y in cards_att[:-1] for x in ["greater", "equal"]] + [x + "(previous, previous2)" for x in ["greater", "equal"]])

    #print(equal(card, prev), card, prev, prev2)

    #TODO: add anything else here that could possibly be a predicate that we split on
    features += ([x(card[:-1], y[:-1]) for y in [prev2, prev] for x in [greater, equal]] + [x(prev[:-1], prev2[:-1]) for x in [greater, equal]])
    ATTRIBUTES += ([x + "(value(current)" + ",value(" + y + ")" for y in cards_att[:-1] for x in ["greater", "equal"]] + [x + "(value(previous), value(previous2))" for x in ["greater", "equal"]])

    # include the classification
    features.append(truth)
    ATTRIBUTES.append("Legal")
    print(len(ATTRIBUTES))

    #print(card, features, len(features))
    return tuple(features)

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
    cards = []

    dt = DecisionTree()

    while(cards_played < 200):
        cards_played += 1

        # somehow choose a card
        card = pick_card()
        print("\nCARD", card)

        # our guess vs. actual truth
        truth = play(card)
        datum = create_datum(card, truth)

        #This should be a fixed constant
        #attrs = [str(i) for i in range(len(datum))]

        if cards_played > 1:
            guess = dt.predict(ATTRIBUTES, [datum])[0]
            if guess == "Null":
                guess = False
        else:
            guess = False

        print("GUESS:", guess)
        print("TRUTH:", truth)

        # TODO: Add the card (and its precessors to the training data set)
        training_data.append(datum)
        cards.append(card)

        # if we are incorrect
        if guess != truth or cards_played == 1:
            print("RE-BUILDING TREE")
            dt.build_tree(training_data, ATTRIBUTES[-1], ATTRIBUTES)
            #dt.print_tree()
            guesses_correct = 0
        # if we guessed right
        else:
            guesses_correct += 1

        # quitting criterion (subject to change)
        if(cards_played > 20 and guesses_correct > 50):
            dt.print_tree()
            print(cards_played)
            return dt, training_data

    print("CARDS PLAYED:", cards_played)
    return dt, training_data, cards

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
    previous  = None
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
    #set_rule("equal(color(previous), color(current))")
    
    
    set_rule("""and(
                        not(and(equal(color(previous), color(previous2)),
                                equal(color(previous), color(current))) ),
                        not(and(equal(value(previous), value(previous2)),
                                equal(value(previous), value(current))) ) )""")
    
    
    print("God chose the rule:")
    print(RULE)
    
    print("Dealing the player a hand...")
    deal_hand()
    print("Players hand is:")
    print(HAND)
    
    BOARD.append(("9D", []))
    BOARD.append(("8H", []))

    dt, training_data, cards = scientist()

    print(boardState())

    # check to make sure the rule fits
    '''
    for t in training_data:
        if(t[-1] != dt.predict(ATTRIBUTES, [t])[0] or t[-1] == False and dt.predict(ATTRIBUTES, [t])[0] == "Null"):
            print("BROKEN")
            index = training_data.index(t)
            print(t, cards[index-2:index+1])
            print(index)
            print(dt.predict(ATTRIBUTES, [t]))
    '''

    #next_card = pick_card_at_random()
    #next_card = pick_card()
    #print("Player is playing:")
    #print(next_card)
    
    #print("God says...")
    #print("Legal") if play(next_card) else print("Illegal")

    #print(boardState())

    """
    rules = []
    rules.append(("equal(color(previous), color(current))", ("9D", "3H")))
    for (r, legal) in rules:
        play_game(r, legal)
    """

main()
