import math
import pdb

class Node():
    value = ""
    children = []
    def __init__(self, val, dictionary):
        self.value = val
        if (isinstance(dictionary, dict)):
            self.children = dictionary.keys()

#Tells which class has majority in given data
def majorClass(attributes, data, target):
    frequency = {}
    index = attributes.index(target)

    for t in data:
        if (t[index] in frequency):
            frequency[t[index]] += 1 
        else:
            frequency[t[index]] = 1

    maximum_value = 0
    # in case there is no data
    major = "Null"

    for key in frequency.keys():
        if frequency[key] > maximum_value:
            maximum_value = frequency[key]
            major = key

    return major

#Calculates Shannon Entropy for data given a target attribute
def entropy(attributes, data, targetAttr):
    #entropy = 0
    frequency = {}
    E = 0.0

    # get the index of the attribute we want to split on
    i = attributes.index(targetAttr)

    #This counts up all of the occurences of the values for attribute i
    for entry in data:
        if entry[i] in frequency:
            frequency[entry[i]] += 1.0
        else:
            frequency[entry[i]]  = 1.0

    # Source: http://pythonfiddle.com/shannon-entropy-calculation/
    #for x in data:
    #    p_x = float(data.count(x[i]) / len(data))
    #    if p_x > 0:
    #        entropy += -p_x * math.log(p_x, 2)

    #return entropy

    for freq in frequency.values():
        E += (-freq/len(data)) * math.log(freq/len(data), 2) 
  
    return E

#Calculates information gain when a particular attribute is chosen for splitting
def information_gain(attributes, data, attr, targetAttr):
    frequency = {}
    subsetEntropy = 0.0
    i = attributes.index(attr)

    # computes the frequencies for each value of attr
    for entry in data:
        if (entry[i] in frequency):
            frequency[entry[i]] += 1.0
        else:
            frequency[entry[i]]  = 1.0

    for val in frequency.keys():
        valProb        = frequency[val] / sum(frequency.values())
        dataSubset     = [entry for entry in data if entry[i] == val]
        subsetEntropy += valProb * entropy(attributes, dataSubset, targetAttr)

    return (entropy(attributes, data, targetAttr) - subsetEntropy)

# Chooses the attribute based on information gain
def choose_best_attribute(data, attributes, target):
    best_attr = attributes[0]
    maxGain = 0
    
    for attr in attributes:
        # don't use the target as an attribute to split on
        if(attr != target):
            newGain = information_gain(attributes, data, attr, target) 
            if newGain > maxGain:
                maxGain = newGain
                best_attr = attr
                
    return best_attr

# Gets unique values for a particular attribute 
def get_values(data, attributes, attr):

    index = attributes.index(attr)
    values_new = list(set([entry[index] for entry in data]))
    values = []

    
    for entry in data:
        if entry[index] not in values:
            values.append(entry[index])
    
    #print(sorted(values))

    if(sorted(values) != sorted(values_new)):
        print("Broken values")
        print(values, values_new)


    return values

#Gets all rows of data where "best" attribute has a value "Value"
def get_data(data, attributes, best, Value):
    index = attributes.index(best)

    new_data = [[]]

    # pretty sure this works
    new_data_x = [tuple(list(entry)[:index] + list(entry)[index+1:]) for entry in data if entry[index] == Value]    
    
    return new_data_x

def recursive_build(data, target, attributes):
    data = data[:]
    vals = [record[attributes.index(target)] for record in data]
    #default = majorClass(attributes, data, target)

    #if not data or (len(attributes) - 1) <= 0:
    #    return default
    if vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        best = choose_best_attribute(data, attributes, target)
        tree = {best:{}}
    
        for val in get_values(data, attributes, best):
            new_data = get_data(data, attributes, best, val)
            newAttr = attributes[:]
            newAttr.remove(best)
            subtree = recursive_build(new_data, target, newAttr)
            tree[best][val] = subtree
    
    return tree

class DecisionTree():

    def build_tree(self, X_train, y_train, attributes):
        self.tree = recursive_build(X_train, y_train, attributes)

    def predict(self, attributes, X_test):
        predictions = []
        
        # if we don't have a dictionary
        if(not isinstance(self.tree, dict)):
            return [self.tree]*len(X_test)
        
        # tree is a dictionary now
        # loop through all of the test data
        for entry in X_test:
            temp_dict = self.tree.copy()
            
            # while we are processing a dictionary, we are at least 
            #   2 levels away from a literal (since each )
            while(isinstance(temp_dict, dict)):

                # grab the only key in this dictionary
                attr = list(temp_dict.keys())[0]
                temp_dict = temp_dict[attr]
                
                # get the attribute index of the attribute in question
                index = attributes.index(attr)
                # get the value for that entry in the test data
                value = entry[index]

                # if our value is in the resulting dictionary
                if(value in temp_dict.keys()):
                    # maybe this is the end
                    res = temp_dict[value]
                    # try and process this (maybe it is a dictionary)
                    temp_dict = temp_dict[value]
                # in general, we don't know what to classify this
                #   TODO: maybe for our case this should be False
                else:
                    res = "Null"
                    break

            # out here, res has the desired value, add to the results
            predictions.append(res)
            
        return predictions
        

    def print_tree(self, t = None, depth = 0):
        if(t == None):
            t = self.tree
        if(isinstance(t, bool)):
            print(t)
            return
        for n in t:
            print(" "*depth + str(n) + ":", end='')
            if(isinstance(t[n], dict)):
                print()
                self.print_tree(t[n], depth+1)
            else:
                print(t[n])

if __name__ == "__main__":
    data = [('0','0','0'),
    ('0','1','1'),
    ('1','0','1'),
    ('1','1','0')]		
    attributes = ['X1','X2','Y']
    target = attributes[-1]	
    X_train = data[:-1]
    X_test = data[-1:]
    tree = DecisionTree()
    tree.build_tree(X_train, target, attributes)
    predictions = tree.predict(attributes,X_test)
    print(predictions)
    print(tree.tree)
    tree.print_tree()

