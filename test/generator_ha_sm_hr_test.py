import matchingproblems
from matchingproblems.generator import generator_ha_sm_hr as generator
import unittest

"""Testing class for the HA, SM, and HR instance generator."""

class TestHaSmHrGenerator(unittest.TestCase):

    def test_instance_generation(self):	
    	gen = generator.Generator_ha_sm_hr()
    	instance = gen.create_instance(
    		n1=3, 
    		n2=4, 
    		pref_lists_residents=[
    			[2, 4, 1],
    			[1, 3],
    			[4, 2]],
    		res_ties=[
    			[1, 0, 1],
    			[1, 0],
    			[0, 1]],
    		pref_lists_hospitals=[
    			[2, 1],
    			[1, 3],
    			[2],
    			[1, 3]],
    		hosp_ties=[
    			[1, 0],
    			[0, 0],
    			[1],
    			[0, 1]],
    		lower_quotas=[1, 1, 0, 0],
    		upper_quotas=[2, 1, 1, 1],
    		instance_info='info')

    	instance_test = (
    		'3 4\n'
    		'1: (2 4) 1\n'
    		'2: (1 3)\n'
    		'3: 4 2\n'
    		'1: 1: 2: (2 1)\n'
    		'2: 1: 1: 1 3\n'
    		'3: 0: 1: 2\n'
    		'4: 0: 1: 1 3\n\n'
    		'info')
    	self.assertEquals(instance, instance_test)
