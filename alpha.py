# ALPHA Eleusis
# CMSC 671
# Dr. M
# 
#Authors:
# Patrick Jenkins
# Leslie McAdoo
# Akshay Subramanya

from new_eleusis import *

#This will hold the representation of all of the cards, 
#   both legal and illegal, that have been played
BOARD = []

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
    pass

def boardState():
    return BOARD


def main():
    rule = parse("equal(color(previous), color(current))")
    print(rule.evaluate((None, "9C", "9S")))

main()