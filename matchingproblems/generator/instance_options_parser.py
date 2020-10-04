import argparse
from argparse import RawTextHelpFormatter

from .enums import *

"""Instance options parser for generating matching instances."""

class Instance_options_parser:
    def check_bounds(self, parser, args):
        """Checks bounds for many input parameters.

        Not all bounds are checked - the user is expected to have some 
        experience with matching problems.

        Args:
          parser: The argument parser.
          args: User input arguments.
        """

        # raise an error if the number of instances requested is less than 1
        if args.numberinstances < 1:
            parser.error('argument -numinst/--numberofinstances: requires an '
                'integer greater than 0.')
        # raise an error if the number of agent 1's requested is less than 1
        if args.n1 < 1:
            parser.error('argument -n1/--numberofagents1: requires an integer '
                'greater than 0.')
        # raise an error if the number of agent 2's requested is specified and 
        # less than 1
        if args.n2 is not None and args.n2 < 1:
            parser.error('argument -n2/--numberofagents2: requires an integer '
                'greater than 0.')
        # raise an error if the number of agent 1's requested is specified and 
        # less than 1
        if args.n3 is not None and args.n3 < 1:
            parser.error('argument -n3/--numberofagents3: requires an integer '
                'greater than 0.')
        # raise an error if the minimum preference list length is either not
        # specified or is less than 1
        if args.minpreflistlength is None or args.minpreflistlength < 1:
            parser.error('argument -pmin/--minpreflistlength: requires an '
                'integer greater than 0.')
        # raise an error if the maximum preference list length is either not
        # specified or is less than 1
        if args.maxpreflistlength is None or args.maxpreflistlength < 1:
            parser.error('argument -pmax/--maxpreflistlength: requires an '
                'integer greater than 0.')
        # raise an error if the maximum preference list length is less than the
        # minimum preference list length
        if args.maxpreflistlength < args.minpreflistlength:
            parser.error('minimum preference list length cannot be greater '
                'than the maximum preference list length')
        # raise an error if the maximum preference list length is greater than n2
        if args.maxpreflistlength > args.n2:
            parser.error('maximum preference list length is greater than the '
                'size of the set of entities to be ranked')
        # raise an error if the first ties probability is not in the range 
        # [0.0, 1.0]
        if args.ties1 < 0.0 or args.ties1 > 1.0:
            parser.error('argument -t1/--ties1: must be in the range '
                '[0.0, 1.0].')
        # raise an error if the second  ties probability is not in the range 
        # [0.0, 1.0]
        if args.ties2 < 0.0 or args.ties2 > 1.0:
            parser.error('argument -t2/--ties2: must be in the range '
                '[0.0, 1.0].')
        # raise an error if the lower quota is specified and less than 0
        if args.lowerquotas < 0:
            parser.error('argument -lq/--lowerquotas: requires an integer of '
                'at least size 0.')
        # raise an error if the lower quota for lecturers is specified and less 
        # than 0
        if args.lecturerlowerquotas < 0:
            parser.error('argument -lql/--lecturerlowerquotas: requires an '
                'integer of at least size 0.')
        # raise an error if the upper quota is specified and is less than n2
        if args.upperquotas is not None and args.upperquotas < args.n2:
            parser.error('argument -uq/--upperquotas: requires an integer of '
                'at least size n2.')
        # raise an error if the lower quota is greater than the upper quota
        if args.lowerquotas > args.upperquotas:
            parser.error('lower quotas cannot be greater than upper quotas')
        # raise an error if the upper quota for lecturers is specified and is 
        # less than 1
        if (args.lecturerupperquotas is not None and 
            args.lecturerupperquotas < 1):
            parser.error('argument -uql/--lecturerupperquotas: requires an '
                'integer of at least size 1.')
        # raise an error if the lecturer targets is less than 0
        if args.lecturertargets < 0:
            parser.error('argument -lt/--lecturertargets: requires an integer '
                'of at least size 0.')
        # raise an error if the lecturer targets is greater than the upper quota
        if (args.lecturertargets is not None and 
            args.lecturerupperquotas is not None and
            args.lecturertargets > args.lecturerupperquotas):
            parser.error('lecturer targets cannot be greater than upper quotas')
        # raise an error if the lower quota is greater than lecturer targets
        if (args.lecturertargets is not None and 
            args.lecturerlowerquotas is not None and
            args.lecturerlowerquotas > args.lecturertargets):
            parser.error('lower quotas cannot be greater than lecturer targets')


    def check_required_and_banned(self, args, parser, matching_problem):
        """Checks required and banned parapters depending on matching problem.

        Args:
          args: User input arguments.
          parser: The argument parser.
          matching_problem: The matching problem in {HA, SM, HR, SPA}
        """
        required_parameters = []
        banned_parameters = []

        # HA
        if matching_problem == Matching_problem.HA:
            required_parameters.extend([
                (args.n1, 'n1'), 
                (args.n2, 'n2'),
                (args.minpreflistlength, 'minpreflistlength'),
                (args.maxpreflistlength, 'maxpreflistlength'),
                (args.upperquotas, 'upperquotas'),
                ])
            banned_parameters.extend([
                (args.twopl, 'twopl'),
                (args.n3, 'n3'),
                (args.ties2, 'ties2'),
                (args.lecturerlowerquotas, 'lecturerlowerquotas'),
                (args.lecturerupperquotas, 'lecturerupperquotas'),
                (args.lecturertargets, 'lecturertargets'),
                ])

        # SM
        if matching_problem == Matching_problem.SM:
            required_parameters.extend([
                (args.n1, 'n1'), 
                (args.minpreflistlength, 'minpreflistlength'),
                (args.maxpreflistlength, 'maxpreflistlength'),
                (args.twopl, 'twopl'),
                ])
            banned_parameters.extend([
                (args.n2, 'n2'),
                (args.n3, 'n3'),
                (args.upperquotas, 'upperquotas'),
                (args.lowerquotas, 'lowerquotas'),
                (args.lecturerlowerquotas, 'lecturerlowerquotas'),
                (args.lecturerupperquotas, 'lecturerupperquotas'),
                (args.lecturertargets, 'lecturertargets'),
                ])

        # HR
        if matching_problem == Matching_problem.HR:
            required_parameters.extend([
                (args.twopl, 'twopl'),
                (args.n1, 'n1'), 
                (args.n2, 'n2'),
                (args.minpreflistlength, 'minpreflistlength'),
                (args.maxpreflistlength, 'maxpreflistlength'),
                (args.upperquotas, 'upperquotas'),
                ])
            banned_parameters.extend([
                (args.n3, 'n3'),
                (args.lecturerlowerquotas, 'lecturerlowerquotas'),
                (args.lecturerupperquotas, 'lecturerupperquotas'),
                (args.lecturertargets, 'lecturertargets'),
                ])

        # SPA-S
        if matching_problem == Matching_problem.SPA:
            required_parameters.extend([
                (args.n1, 'n1'), 
                (args.n2, 'n2'),
                (args.n3, 'n2'),
                (args.minpreflistlength, 'minpreflistlength'),
                (args.maxpreflistlength, 'maxpreflistlength'),
                (args.upperquotas, 'upperquotas'),
                (args.lecturerupperquotas, 'lecturerupperquotas'),
                ])

        # Check that required parameters are present.
        for req in required_parameters:
            if req[0] == parser.get_default(req[1]):
                parser.error('you must use all required parameters for problem '
                    'type ' + str(matching_problem))

        # Check that banned parameters are not present.
        for ban in banned_parameters:
            if not ban[0] == parser.get_default(ban[1]):
                parser.error('you are using a banned parameter for problem '
                    'type ' + str(matching_problem))

        

    def get_matching_problem(self, args):
        """Return the matching problem as an enum.

        Args:
          args: User input arguments.

        Return:
          The matching problem as an enum.
        """
        if args.matchingproblem == 'ha':
            return Matching_problem.HA
        if args.matchingproblem == 'sm':
            return Matching_problem.SM
        if args.matchingproblem == 'hr':
            return Matching_problem.HR
        if args.matchingproblem == 'spa':
            return Matching_problem.SPA


    def set_defaults(self, matching_problem, args):
        """Set the default value for several parameters.

        Args:
          matching_problem: The matching problem in {HA, SM, HR, SPA}
          args: User input arguments.
        """

        if matching_problem == Matching_problem.SM:
            args.n2 = args.n1
        if args.lowerquotas == None:
            args.lowerquotas = 0
        if args.lecturerlowerquotas == None:
            args.lecturerlowerquotas = 0
        if args.ties1 == None:
            args.ties1 = 0.0
        if args.ties2 == None:
            args.ties2 = 0.0
        if args.lecturertargets == None:
            args.lecturertargets = 0.0
        if args.skew == None:
            args.skew = 1.0


    def parse(self, arguments):
        """Parse the command line arguments.

        Args:
          arguments: User given command line arguments.

        Returns:
          The parsed arguments.
        """
        parser = argparse.ArgumentParser(
            description='Generates matching problem instances.',
            formatter_class=RawTextHelpFormatter)
        parser.add_argument(
            '-numinst',
            '--numberinstances', 
            action='store', 
            dest='numberinstances',
            help=('total number of instances to generate'),
            required=True,
            type=int)
        parser.add_argument(
            '-o',
            '--outputdirectory', 
            action='store', 
            dest='outputdirectory',
            help=('output directory'),
            required=True,
            type=str)
        parser.add_argument(
            '-mp', 
            '--matchingproblem', 
            action='store', 
            choices=['ha', 'sm', 'hr', 'spa'],
            dest='matchingproblem',
            help=('matching problem type, where\n'
                '* ha = House Allocation problem (HA) and variants\n'
                '* sm = Stable Marriage problem (SM) and variants\n'
                '* hr = hospital/residents problem (HR) and variants\n'
                '* spas = Student-Project Allocation problem (SPA) and '
                'variants\n'),
            required=True,
            type=str)
        parser.add_argument(
            '-twopl',
            '--preferencelists2', 
            action='store_true', 
            dest='twopl',
            help=('Preference lists on both sides of the matching problem'))
        parser.add_argument(
            '-skew',
            '--linearskew', 
            action='store', 
            dest='skew',
            help=('linear skew for preference lists, a value of x indicates \n'
                'that the most popular agent is x times more popular than \n'
                'the least'),
            type=float)
        parser.add_argument(
            '-n1',
            '--numberofagents1', 
            action='store', 
            dest='n1',
            help=('number of applicants (HA) / men (SM) / residents (HR) / \n'
                'students (SPA)'),
            type=int)
        parser.add_argument(
            '-n2',
            '--numberofagents2', 
            action='store', 
            dest='n2',
            help=('number of houses (HA) / hospitals (HR) / projects (SPA)'),
            type=int)
        parser.add_argument(
            '-n3',
            '--numberofagents3', 
            action='store', 
            dest='n3',
            help=('number of lecturers (SPA)'),
            type=int)
        parser.add_argument(
            '-pmin',
            '--minpreflistlength', 
            action='store', 
            dest='minpreflistlength',
            help=('minimum size of preference lists for applicants (HA) / \n'
                'men (SM) / residents (HR) / students (SPA)'),
            type=int)
        parser.add_argument(
            '-pmax',
            '--maxpreflistlength', 
            action='store',
            dest='maxpreflistlength',
            help='maximum size of preference lists for applicants (HA) / \n'
                'men (SM) / residents (HR) / students (SPA)',
            type=int)
        parser.add_argument(
            '-t1',
            '--ties1', 
            action='store', 
            dest='ties1',
            help='probability of ties for applicants (HA) / men (SM) / \n'
                'residents (HR) / students (SPA) [0.0, 1.0]',
            type=float)
        parser.add_argument(
            '-t2',
            '--ties2', 
            action='store', 
            dest='ties2',
            help=('probability of ties for women (SM) / hospitals (HR) / \n'
                'lecturers (SPA) [0.0, 1.0]'),
            type=float)
        parser.add_argument(
            '-lq',
            '--lowerquotas', 
            action='store', 
            dest='lowerquotas',
            help=('lower quotas for houses (HA) / hospitals (HR) / projects '
                '(SPA)'),
            type=int)
        parser.add_argument(
            '-llq',
            '--lecturerlowerquotas', 
            action='store', 
            dest='lecturerlowerquotas',
            help=('lower quotas for lecturers (SPA)'),
            type=int)
        parser.add_argument(
            '-uq',
            '--upperquotas', 
            action='store', 
            dest='upperquotas',
            help=('upper quotas for houses (HA) / hospitals (HR) / projects '
                '(SPA)'),
            type=int)
        parser.add_argument(
            '-luq',
            '--lecturerupperquotas', 
            action='store', 
            dest='lecturerupperquotas',
            help=('upper quotas for lecturers (SPA)'),
            type=int)
        parser.add_argument(
            '-lt',
            '--lecturertargets', 
            action='store', 
            dest='lecturertargets',
            help=('targets for lecturers (SPA)'),
            type=int)
        
        args = parser.parse_args(arguments)
        matching_problem = self.get_matching_problem(args)
        self.check_required_and_banned(args, parser, matching_problem)
        self.set_defaults(matching_problem, args)
        self.check_bounds(parser, args)
        
        return args
