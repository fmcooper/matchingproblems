import matchingproblems
from matchingproblems.generator import generator_spa as generator
import unittest

"""Testing class for the SPA instance generator."""

class TestSPAGenerator(unittest.TestCase):

    def test_instance_generation(self):	
    	gen = generator.Generator_spa()
    	instance = gen.create_instance(
    		n1=3, 
    		n2=4, 
            n3=2,
    		pref_lists_students=[
    			[2, 4, 1],
    			[1, 3],
    			[4, 2]],
    		st_ties=[
    			[1, 0, 1],
    			[1, 0],
    			[0, 1]],
            project_lecturers=[1, 1, 2, 2],
            lower_quotas=[1, 1, 0, 0],
            upper_quotas=[2, 1, 1, 1],
    		pref_lists_lecturers=[
    			[2, 1, 3],
    			[1, 3, 2]],
    		lec_ties=[
    			[1, 0, 1],
    			[1, 1, 1]],
            lec_lower_quotas=[1, 0],
            lec_targets=[1, 1],
            lec_upper_quotas=[2, 2],
    		instance_info='info')

    	instance_test = (
    		'3 4 2\n'
    		'1: (2 4) 1\n'
    		'2: (1 3)\n'
    		'3: 4 2\n'
    		'1: 1: 2: 1\n'
    		'2: 1: 1: 1\n'
    		'3: 0: 1: 2\n'
    		'4: 0: 1: 2\n'
            '1: 1: 1: 2: (2 1) 3\n'
            '2: 0: 1: 2: (1 3 2)\n\n'
    		'info')

    	self.assertEquals(instance, instance_test)
