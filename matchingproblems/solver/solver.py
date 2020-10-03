from .enums import *
from .fileIO import import_model
from .model import Model
from .options_parser import Options_parser
from .lp_solver import LP_Solver
from .brute_force_solver import Brute_force_solver
# from .solver import Solver

import datetime

"""The Solver controller API class and creation function.

The Solver class defines the API for users to access the IP solver.
"""

"""Function to return a new Solver controller."""
def create(filename):
        return Solver(filename)

""" The Solver controller API class.

    The Solver class defines the API for users to access the IP solver.
    """

class Solver:

    def __init__(self, args):
        '''Constructs a Solver controller.

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

        
    def solve(self, msg=False, timeLimit=None, threads=None, write=False):
        '''Solves the SPA-STL instance.

        Args:
          msg: Pulp indicator as to whether the solver should output info.
          timeLimit: Pulp time limit for optimisations (note this will be for 
            each individual optimisation, exceeding the overall time limit will
            be dealt with in another part of the program).
          threads: Pulp variable for the number of threads to use when solving.
          write: Indicates whether the model should be written to file.
        '''

        # Brute force method.
        if self.options_parser.solver_options[Solver_options.BRUTEFORCE]:
            self.solver = Brute_force_solver(
                self.options_parser.instance_options,
                self.model)
        # Pulp LP solver method.
        else:
            self.solver = LP_Solver(
                self.model,
                self.options_parser.instance_options,
                self.options_parser.extra_constraints,
                self.options_parser.optimisation_options)
        
        self.model.time_limit = timeLimit

        time_after_model_creation = datetime.datetime.now()
        self.model.time_after_model_creation = time_after_model_creation
        
        if self.options_parser.solver_options[Solver_options.BRUTEFORCE]:
            pulp_status = self.solver.run()
        else:
            pulp_status = self.solver.run(msg, timeLimit, threads, write)
            self.model.pulp_status = pulp_status

        time_after_solve = datetime.datetime.now()
        self.model.time_after_solve = time_after_solve


    def get_debug(self):
        
        '''Returns debugging information from the solver.

        Returns:
            Debugging information from the solver.
        '''
        return self.model.get_debug()


    def get_results(self):
        '''Returns condenced results.

        Returns:
            Condenced results.
        '''

        if self.options_parser.solver_options[Solver_options.BRUTEFORCE]:
            return self.solver.get_results()
        else:
            return self.get_results_short()


    def get_results_short(self):
        '''Returns condenced results.

        Returns:
            Condenced results.
        '''

        stable_correctness = False
        if self.options_parser.extra_constraints[Extra_constraints.STAB]: 
            stable_correctness = True
        return self.model.get_results(Output_type.SHORT, stable_correctness)


    def get_results_long(self):
        '''Returns long form results.

        Returns:
            Long form results.
        '''

        stable_correctness = False
        if self.options_parser.extra_constraints[Extra_constraints.STAB]: 
            stable_correctness = True
        return self.model.get_results(Output_type.LONG, stable_correctness)
