import matchingproblems
from matchingproblems.solver import options_parser as op
from matchingproblems.solver import enums
import unittest

"""Testing class for options parser."""

class TestParser(unittest.TestCase):

    def test_get_ordered_optimisations(self):
        optimisation_tuples = [
            (4, enums.Optimisation_options.MAXSIZE), 
            (2, enums.Optimisation_options.MINSIZE), 
            (None, enums.Optimisation_options.GENEROUS), 
            (5, enums.Optimisation_options.GREEDY), 
            (None, enums.Optimisation_options.MINCOST), 
            (1, enums.Optimisation_options.MINSQCOST), 
            (3, enums.Optimisation_options.LOADMAXBAL), 
            (None, enums.Optimisation_options.LOADSUMBAL), 
            ]

        parser = op.Options_parser()
        ordered, count = parser._get_ordered_optimisations(optimisation_tuples)
        
        answer = [
            enums.Optimisation_options.MINSQCOST,
            enums.Optimisation_options.MINSIZE,
            enums.Optimisation_options.LOADMAXBAL,
            enums.Optimisation_options.MAXSIZE,
            enums.Optimisation_options.GREEDY,
            ]

        self.assertEqual(ordered, answer)

        self.assertEqual(count, 5)

