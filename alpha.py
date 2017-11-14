"""
ALPHA Eleusis
CMSC 671
Dr. Matuszek
 
Authors:
    Patrick Jenkins
    Leslie McAdoo
    Akshay Subramanya
"""

from new_eleusis import *
import random

#This will hold the representation of all of the cards, 
#   both legal and illegal, that have been played
BOARD = []
RULE = None
HYPOTHESIS = None
HAND = []

def __pick_card():
    """
    Helper function that picks a card from the HAND, for Phase I, the hand
    includes all possible cards
    
    TODO: Phase II gamification
    """
    for card in HAND:
        # if card is illegal under the hypothesis, play it
        if not HYPOTHESIS.evaluate(card):
            # TODO: phase II should remove the card from the hand
            return card
        
    return __pick_card_at_random()

def __pick_card_at_random():
    """
    Helper function that returns a random card from the hand
    """
    suits = ['C', 'D', 'H', 'S']
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    # TODO: Phase II should remove the played card from the hand
    return random.choice(HAND) if HAND else (random.choice(suits), random.choice(values))

def deal_hand():
    """
    Deals a hand to the player, if this is phase one, this is every possible card
    """
    # TODO: Phase II
    for suit in ['C', 'D', 'H', 'S']:
        for value in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
            HAND.append((suit, value))

def create_datum(card):
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
    individuals = [suit, even, color]

    features = [x(y) for y in cards for x in individuals]
    print(features)

    return features

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

    while(cards_played < 200):
        cards_played += 1

        # somehow choose a card
        card = __pick_card()

        # our guess vs. actual truth
        guess = HYPOTHESIS.evaluate(card)
        truth = play(card)

        # TODO: Add the card (and its precessors to the training data set)
        training_data.append(create_datum(card))

        # if we are incorrect
        if(guess != truth):
            # will be a DT method
            retrain(training_data)
            guesses_correct = 0
        # if we guessed right
        else:
            guesses_correct += 1


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

def main():
    set_rule("equal(color(previous), color(current))")
    deal_hand()
    print(RULE)
    BOARD.append(("9D", []))
    #BOARD.append(("5C", []))

    print(play("AC"))
    print(play("5H"))

    create_datum("6D")

    print(boardState())

main()