from .instance_options_parser import Instance_options_parser
from .enums import *
from .generator_ha_sm_hr import Generator_ha_sm_hr
from .generator_spa import Generator_spa

"""The Generator controller API class and creation function.

The Generator class defines the API for users to access the Generator.
"""

"""Function to return a new Generator controller."""
def create(args):
    return Generator(args)


class Generator:

    def __init__(self, args):
        self.options_parser = Instance_options_parser()
        self.args = self.options_parser.parse(args)
        matching_problem = self.options_parser.get_matching_problem(self.args)

        if matching_problem in [
            Matching_problem.HA,
            Matching_problem.SM,
            Matching_problem.HR]:
            generator_hr = Generator_ha_sm_hr()
            generator_hr.generate_instances(self.args)
        elif matching_problem in [
            Matching_problem.SPA]:
            generator_spa = Generator_spa()
            generator_spa.generate_instances(self.args)
