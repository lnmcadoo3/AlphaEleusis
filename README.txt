ALPHA ELEUSIS

Authors:
	Patrick Jenkins
	Leslie McAdoo
	Akshayvarun Subramanya
	
Description:
	Alpha Eleusis is a Python3 implementation of a New Eleusis player. It uses a decision tree to make inferences
about which cards are legal or illegal. Whenever the player guesses the legality of the card incorrectly the tree
retrains itself on all given data in order to create the simplest hypothesis possible. For Phase 1, the player
plays at random, but in Phase 2 we will implement some smarter strategies. We wanted to make sure the AI core of
our system was in place before we started refining and improving the other aspects of its play.