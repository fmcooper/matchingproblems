from enum import Enum

class Instance_options(Enum):
    NUMAGENTS = 1       # number of agents in the instance (2 or 3)
    TWOPL = 2           # indicates if two sided preference lists are present
    PC = 3              # project closures present

class Extra_constraints(Enum):
    STAB = 1            # stability constraints

class Optimisation_options(Enum):
    MAXSIZE = 1         # maximising number of assigned students
    MINSIZE = 2         # minimising number of assigned students
    GENEROUS = 3        # generous optimisation
    GREEDY = 4          # greedy optimisation
    MINCOST = 5         # minimising sum of ranks of matched students
    MINSQCOST = 6       # minimising sum of squares of ranks of matched students
    LOADMAXBAL = 7      # load max balancing for lecturers
    LOADSUMBAL = 8      # load sum balancing for lecturers

class Optimisation_type(Enum):
    MAXIMISE = 1        # maximising the objective function
    MINIMISE = 2        # minimising the objective function

class Output_type(Enum):
    SHORT = 1           # short results output
    LONG = 2            # long results output

class Solver_options(Enum):
    BRUTEFORCE = 1      # solve using brute force
