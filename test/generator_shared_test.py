import matchingproblems
from matchingproblems.generator import generator_shared as generator
import unittest
import numpy as np

"""Testing class for the SPA instance generator."""

class TestGeneratorShared(unittest.TestCase):

    def test_create_linear_distribution(self):	
    	dist = generator.create_linear_distribution(number_agents=4, skew=10.0)
    	dist_test = np.asarray([
            0.045454545454545456, 
            0.18181818181818182, 
            0.3181818181818182, 
            0.45454545454545453])

    	self.assertListEqual(list(dist), list(dist_test))


    def test_create_quotas(self):
        quotas = generator.create_quotas(n=4, sum_q=6)
        self.assertListEqual(quotas, [2, 2, 1, 1])


    def test_create_string_pref(self):    
        pref_list_string = generator.create_string_pref(
            pref_list=[1, 2, 3, 4], 
            ties_indicators=[0, 1, 0, 1])
        self.assertEqual(pref_list_string, ['1','(2', '3)', '4'])


