# ALPHA Eleusis
# CMSC 671
# Dr. Matuszek
# 
#Authors:
# Patrick Jenkins
# Leslie McAdoo
# Akshay Subramanya

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
        if HYPOTHESIS:
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

def scientist():
    rule = None
    cards_played = 0

    while(not rule and cards_played < 200):
        cards_played += 1

        #Quitting criterion
        if(cards_played > 20):
            pass

    return rule

def score():
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
    return BOARD

def set_rule(rule):
    #Maybe there's a better way to do this
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

    print(boardState())

main()