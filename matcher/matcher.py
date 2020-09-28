from .enums import *
from .fileIO import import_model
from .model import Model
from .options_parser import Options_parser
from .solver import Solver

import datetime

"""The Matcher controller API class and creation function.

The Matcher class defines the API for users to access the IP solver.
"""

"""Function to return a new Matcher coltroller."""
def create(filename):
        return Matcher(filename)

""" The Matcher controller API class.

    The Matcher class defines the API for users to access the IP solver.
    """

class Matcher:

    def __init__(self, args):
        '''Constructs a Matcher controller.

        Args: 
            args: Command line options.
        '''

        time_start = datetime.datetime.now()
        self.options_parser = Options_parser()
        self.options_parser.parse(args)
        self.model = import_model(
            self.options_parser.filename,
            self.options_parser.instance_options)
        self.model.time_start = time_start

        
    def solve(self, msg=False, timeLimit=None, threads=None):
        '''Solves the SPA-STL instance.'''
        self.solver = Solver(
            self.model,
            self.options_parser.instance_options,
            self.options_parser.extra_constraints,
            self.options_parser.optimisation_options)
        self.model.time_limit = timeLimit

        time_after_model_creation = datetime.datetime.now()
        self.model.time_after_model_creation = time_after_model_creation
        
        pulp_status = self.solver.run(msg, timeLimit, threads)
        self.model.pulp_status = pulp_status

        time_after_solve = datetime.datetime.now()
        self.model.time_after_solve = time_after_solve


    def get_debug(self):
        '''Returns debugging information from the solver.

        Returns:
            Debugging information from the solver.
        '''
        return self.model.get_debug()


    def get_results_short(self):
        '''Returns condenced results.

        Returns:
            Condenced results.
        '''
        return self.model.get_results(Output_type.SHORT)

    def get_results_long(self):
        '''Returns long form results.

        Returns:
            Long form results.
        '''
        return self.model.get_results(Output_type.LONG)
