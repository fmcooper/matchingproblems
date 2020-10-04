import argparse
from argparse import RawTextHelpFormatter
from .enums import *

"""Options parser for solving matching instances."""

class Options_parser:
    def _create_arg_parser(self):
        """Returns an argument parser.

        Returns:
          An argument parser.
        """
        parser = argparse.ArgumentParser(
            description='Solves matching problem instances.',
            formatter_class=RawTextHelpFormatter)
        # filename
        parser.add_argument(
            '-f',
            '-filename',
            action='store',
            dest='filename',
            help=('input file name'),
            required=True)
        # filename
        parser.add_argument(
            '-na',
            '-numagents',
            action='store',
            dest='numagents',
            help=('number of agents in the instance (2 for HR, 3 for SPA)'),
            required=True,
            type=int)
        # hospital or lecturer preference lists
        parser.add_argument(
            '-twopl',
            '-twosidedpreferencelists',
            action='store_true',
            dest='twopl',
            help=('women (SM), hospital (HR) or lecturer (SPA) preference lists present'))
        # project closures
        parser.add_argument(
            '-pc',
            '-projectclosures',
            action='store_true',
            dest='pc',
            help=('project closures allowed'))
        # stability
        parser.add_argument(
            '-stab',
            '-stability', 
            action='store_true',
            dest='stab',
            help=('add stability constraints'))
        # maximise size
        parser.add_argument(
            '-maxsize',
            '-maximisesize', 
            action='store',
            dest='maxsize',
            help=('maximise size at the given optimisation position'),
            type=int)
        # minimise size
        parser.add_argument(
            '-minsize',
            '-minimisesize', 
            action='store',
            dest='minsize',
            help=('minimise size at the given optimisation position'),
            type=int)
        # generous
        parser.add_argument(
            '-gen',
            '-generous', 
            action='store',
            dest='gen',
            help=('performs generous optimisation at the given optimisation ' +
                'position'),
            type=int)
        # greedy
        parser.add_argument(
            '-gre',
            '-greedy', 
            action='store',
            dest='gre',
            help=('performs greedy optimisation at the given optimisation ' +
                'position'),
            type=int)
        # minimises cost
        parser.add_argument(
            '-mincost',
            '-minimisecost', 
            action='store',
            dest='mincost',
            help=('minimise cost at the given optimisation position'),
            type=int)
        # minimises sum of costs squared
        parser.add_argument(
            '-minsqcost',
            '-minimisesquaredcost', 
            action='store',
            dest='minsqcost',
            help=('minimises sum of squares of costs at the given ' +
                'optimisation position'),
            type=int)
        # load max balanced
        parser.add_argument(
            '-lmb',
            '-loadmaxbalanced', 
            action='store',
            dest='lmb',
            help=('minimises the maximum absolute difference between ' +
                'lecturer occupancy and target at the given optimisation ' +
                'position'),
            type=int)
        # load sum balanced
        parser.add_argument(
            '-lsb',
            '-loadsumbalanced', 
            action='store',
            dest='lsb',
            help=('minimises the sum of absolute differences between ' +
                'lecturer occupancies and targets at the given optimisation ' +
                'position'),
            type=int)
        # load sum balanced
        parser.add_argument(
            '-bf',
            '-bruteforce', 
            action='store_true',
            dest='bruteforce',
            help=('solve using a brute force method'))
        return parser


    def _get_instance_options(self, args):
        """Returns user chosen instance options.

        Returns:
          User chosen instance options.
        """

        return {
            Instance_options.TWOPL : args.twopl,
            Instance_options.NUMAGENTS : args.numagents,
            Instance_options.PC : args.pc,
            }


    def _get_solver_options(self, args):
        """Returns user chosen solver options.

        Returns:
          User chosen solver options.
        """

        return {
            Solver_options.BRUTEFORCE : args.bruteforce,
            }


    def _get_extra_constraints(self, args):
        """Returns user chosen extra constraint options.

        Returns:
          User chosen extra constraint options.
        """
        return {
            Extra_constraints.STAB : args.stab,
            }


    def _get_optimisation_tuples(self, args):
        """Returns user chosen optimisation options as tuples.

        Returns:
          User chosen optimisation options.
        """

        return [
            (args.maxsize, Optimisation_options.MAXSIZE), 
            (args.minsize, Optimisation_options.MINSIZE), 
            (args.gen, Optimisation_options.GENEROUS), 
            (args.gre, Optimisation_options.GREEDY), 
            (args.mincost, Optimisation_options.MINCOST), 
            (args.minsqcost, Optimisation_options.MINSQCOST), 
            (args.lmb, Optimisation_options.LOADMAXBAL), 
            (args.lsb, Optimisation_options.LOADSUMBAL), 
            ]


    def _get_ordered_optimisations(self, opts):
        """Returns ordered optimisations.

        Returns:
          Ordered optimisations
        """

        ordered_opts = len(opts) * [0]
        count = 0
        for ordinal, opt in opts:
            if not ordinal == None:
                count += 1
                ordered_opts[ordinal - 1] = opt
        temp = []
        for i in range(len(ordered_opts)):
            if not ordered_opts[i] == 0:
                temp.append(ordered_opts[i])
        ordered_opts = temp
        return ordered_opts, count


    def _stability_requirements_check(
        self, parser, instance_options, extra_constraints):
        """Checks that stability requirements are met.

        Args:
          parser: The argument parser.
          instance_options: User chosen instance options.
          extra_constraints: User chosen extra constraint options.
        """
        if (extra_constraints[Extra_constraints.STAB] and 
            not instance_options[Instance_options.TWOPL]):
            parser.error('must have two sided preference lists when choosing '
                'stability')


    def _get_and_check_orderings(self, parser, args):
        """Checks and returns ordered optimisations.

        Returns:
          Ordered optimisations.
        """
        opts = self._get_optimisation_tuples(args)

        # Raise an error if any of the user given optimisations orderings less  
        # than 1 or more than len(optimisations).
        for ordering, opt in opts:
            if not ordering == None:
                if ordering < 1 or ordering > len(opts):
                    parser.error('orderings for optimisations must be ' +
                        'between 0 and ' + str(len(opts)))

        ordered_opts, count = self._get_ordered_optimisations(opts)

        # Raise an error if there are repeated values in the optimisation 
        # orders.
        if not len(ordered_opts) == count:
            parser.error('cannot have repeated positional arguments for' +
                'optimisations')

        return ordered_opts


    def parse(self, arguments):
        """Parses the user given command line arguments."""
        parser = self._create_arg_parser()
        args = parser.parse_args(arguments)
        self.filename = args.filename
        self.instance_options = self._get_instance_options(args)
        self.solver_options = self._get_solver_options(args)
        self.extra_constraints = self._get_extra_constraints(args)
        self.optimisation_options = self._get_and_check_orderings(parser, args)
        self._stability_requirements_check(
            parser, self.instance_options, self.extra_constraints)
