ALPHA ELEUSIS

Authors:
	Patrick Jenkins
	Leslie McAdoo
	Akshayvarun Subramanya
	
Description:
	Alpha Eleusis is a Python3 implementation of a New Eleusis player. It uses a decision tree to make inferences
about which cards are legal or illegal. Whenever the player guesses the legality of the card incorrectly the tree
retrains itself on all given data in order to create the simplest hypothesis possible. The confidence measure of our algorithm is basically based on the number of cards(n) it makes a correct prediciton. Currently n=20.
Based on the guidelines provided for the scoring function, we have modified the program to include adversaries so the game is now in a multi-player setting. When a rule is predicted, we check for the equivalency with the actual rule in an exhaustive fashion i.e run all combinations of three cards for both rules.

To change God's rule, modify lines 78 and 79 in game.py to your rule and an initial 3 cards that are dealt

# Set a rule for testing
rule = "equal(color(previous), color(current))"
cards = ["10H", "2D", "4H"]

***
We need game_ended to be passed in as true at the end, otherwise our code will not work.
***

Usage:
	python3   game.py
