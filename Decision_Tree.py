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
    major = ""

    for key in frequency.keys():
        if frequency[key]>maximum_value:
            maximum_value = frequency[key]
            major = key

    return major

#Calculates Shannon Entropy for data given a target attribute
def entropy(attributes, data, targetAttr):

    frequency = {}
    E = 0.0

    i = 0
    for entry in attributes:
        if (targetAttr == entry):
            break
        i = i + 1

    #i = i - 1
    for entry in data:
        if (entry[i] in frequency):
            frequency[entry[i]] += 1.0
        else:
            frequency[entry[i]]  = 1.0

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
    maxGain = 0;
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
    values = []

    for entry in data:
        if entry[index] not in values:
            values.append(entry[index])

    return values

#Gets all rows of data where "best" attribute has a value "Value"
def get_data(data, attributes, best, Value):
    new_data = [[]]
    index = attributes.index(best)

    for entry in data:
        if (entry[index] == Value):
            newEntry = []
            for i in range(0,len(entry)):
                if(i != index):
                    newEntry.append(entry[i])
            new_data.append(newEntry)

    new_data.remove([])    
    return new_data

def recursive_build(data,target,attributes):
    data = data[:]
    vals = [record[attributes.index(target)] for record in data]
    default = majorClass(attributes, data, target)

    if not data or (len(attributes) - 1) <= 0:
        return default
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        best = choose_best_attribute(data, attributes, target)
        tree = {best:{}}
    
        for val in get_values(data, attributes, best):
            new_data = get_data(data, attributes, best, val)
            newAttr = attributes[:]
            newAttr.remove(best)
            subtree = recursive_build(new_data,target,newAttr)
            tree[best][val] = subtree
    
    return tree


class DecisionTree():

    def build_tree(self,X_train,y_train,attributes):
        self.tree  = recursive_build(X_train,y_train,attributes)

    def predict(self,attributes,X_test):
        predictions = []
        res = ""
        for entry in X_test:
            temp_dict = self.tree.copy()
        while(isinstance(temp_dict, dict)):
            root = Node(list(temp_dict.keys())[0], temp_dict[list(temp_dict.keys())[0]])
            temp_dict = temp_dict[list(temp_dict.keys())[0]]
            index = attributes.index(root.value)
            value = entry[index]
            if(value in temp_dict.keys()):
                child = Node(value, temp_dict[value])
                res = temp_dict[value]
                temp_dict = temp_dict[value]
            else:
                res = "Null"
                break
        predictions.append(res)
        return predictions

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
