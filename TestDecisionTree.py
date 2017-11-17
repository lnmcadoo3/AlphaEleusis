'''

'''

import unittest
import Decision_Tree

class TestDecisionTree(unittest.TestCase):
    
    def test_entropy(self):
        attributes = []
        data = []
        targetAttr = ''
        
        self.assertEqual(Decision_Tree.entropy(attributes, data, targetAttr), 0)
    
    def test_information_gain(self):
        attributes = []
        data = []
        attr = ''
        targetAttr = ''
        
        self.assertEqual(Decision_Tree.information_gain(attributes, data, attr, targetAttr), 0)
    
if __name__ == '__main__':
    unittest.main()
        