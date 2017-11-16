import numpy as np
import pdb
##helper functions##
#Partition function -  maps the inputs to its unique values
def partition(a):
	ret = dict()
	for i in np.unique(a):
		ret[i] = (a==i).nonzero()[0]
	return ret 

#Entropy calculation - for a given sequence of values, counts number of occurences, calculates the probabilty and measures the entropy.(sum(-plog2p))
def entropy(s):
    E = 0
    val, counts = np.unique(s, return_counts=True)
    probs = counts.astype('float')/len(s)
    for p in probs:
        if p != 0.0:
            E -= p * np.log2(p)
    return E

def information_gain(Y, X):

    IG = entropy(Y)

    # Partition x, according to attribute values x_i
    val, counts = np.unique(X, return_counts=True)
    freqs = counts.astype('float')/len(X)

    # Calculate a weighted average of the entropy

    for p, v in zip(freqs, val):
        IG -= p * entropy(Y[X == v])

    return IG

def attr_choose(X, Y):

    gain = []
    for x_attr in X.T:
    	gain.append(information_gain(Y, x_attr))
    gain = np.asarray(gain)
    best = np.argmax(gain)
    return best

def is_leaf(s):
    return len(set(s)) == 1

def recursive_build(data, target):
    #Base case:if no split is possible in labels then return the set
	if is_leaf(target) or len(target) == 0:
		return target
    

##class definition
class Decision_tree:
	
	def __init__(self):
		"""
		Creates the decision tree
		"""
		print('Creating Decision Tree')

	def build_tree(self,X_train,y_train):
		
		return recursive_build(X_train,y_train)


	#def predict(self,X_test):
	#	predictions = []
	#	for x in X_test:

	#		predictions.append()

	#	return predictions


	#def get_rule(self):







