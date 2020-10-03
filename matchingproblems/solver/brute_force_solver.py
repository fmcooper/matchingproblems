from .enums import *

from itertools import product
from pulp import *

"""Brute force solver for an instance of SPA-STL.

SPA-STL is the Student-Project Allocation problem with lecturer preferences over
Students including Ties and Lecturer targets.
"""

class Brute_force_solver:
    """ Brute force solver for an instance of SPA-STL.

    Attributes:
        model: Model representing an SPA-STL instance.
        instance_options: User chosen instance options.
        solver: The Pulp solver.
    """
    def __init__(
        self, 
        instance_options, 
        model):
        """Constructor for the Solver.

        Args:
            model: Model representing an SPA-STL instance. 
        """

        self.model = model
        self.instance_options = instance_options


    def run(self):
        """Run the solver."""

        num_students = self.model.num_students
        num_projects = self.model.num_projects
        num_lecturers = self.model.num_lecturers

        self.optimal_size = -1
        self.optimal_maxsizemincost = (
            self.model.num_projects * self.model.num_students)
        self.optimal_maxsizeminsqcost = (
            pow(self.model.num_projects, 2) * self.model.num_students)
        self.optimal_maxsizemindegree = self.model.num_projects
        self.optimal_generousmaxprofile = []
        self.optimal_greedymaxprofile = []
        self.optimal_greedyprofile = [0] * num_students
        self.optimal_max_lec_abs_diff = self.model.get_max_lec_upper_quota()
        self.optimal_sum_lec_abs_diff = (
            self.model.get_max_lec_upper_quota() * num_lecturers)

        # iterate over each possible matching
        for matching in (
            product(list(range(num_projects + 1)), repeat=num_students)):
            

            # if the matching is valid, add to model and retrieve all optimal
            # measures
            matching_pairs = self.get_matching_pairs(matching)
            # print("considering matching: ", matching)
            if self.is_valid(matching_pairs):
                size = len(matching_pairs)
                cost = self.model._get_cost(matching_pairs)
                costsq = self.model._get_cost_sq(matching_pairs)
                degree = self.model._get_degree(matching_pairs)
                profile = self.model._get_profile(matching_pairs)
                max_lec_abs_diff = self.model._get_max_lec_abs_diff(
                    matching_pairs)
                sum_lec_abs_diff = self.model._get_sum_lec_abs_diff(
                    matching_pairs)


                # save larger size
                if size > self.optimal_size:
                    self.optimal_size = size
                    self.optimal_maxsizemincost = cost
                    self.optimal_maxsizemindegree = degree
                    self.optimal_maxsizeminsqcost = costsq
                    self.optimal_generousmaxprofile = profile
                    self.optimal_greedymaxprofile = profile

                # same size
                if size == self.optimal_size:
                    if cost < self.optimal_maxsizemincost:
                        self.optimal_maxsizemincost = cost
                    if degree < self.optimal_maxsizemindegree:
                        self.optimal_maxsizemindegree = degree
                    if costsq < self.optimal_maxsizeminsqcost:
                        self.optimal_maxsizeminsqcost = costsq
                    if self.moregen(profile, self.optimal_generousmaxprofile):
                        self.optimal_generousmaxprofile = profile
                    if self.moregre(profile, self.optimal_greedymaxprofile):
                        self.optimal_greedymaxprofile = profile

                # save greedy
                if self.moregre(profile, self.optimal_greedyprofile):
                    self.optimal_greedyprofile = profile

                # save minimum max lec abs diff
                if max_lec_abs_diff < self.optimal_max_lec_abs_diff:
                    self.optimal_max_lec_abs_diff = max_lec_abs_diff

                # save minimum sum lec abs diff
                if sum_lec_abs_diff < self.optimal_sum_lec_abs_diff:
                    self.optimal_sum_lec_abs_diff = sum_lec_abs_diff


    def get_results(self):
        """Returns a string containing the results of the run.

        Returns:
          String output results for the run.
        """

        # Header.
        start_time_string = self.model.time_start.strftime("%d %b %Y, %X %Z")
        results = ('# Results for the run conducted on ' 
            + start_time_string + '\n\n')

        # Timings calculations.
        time_model_creation = (
            self.model.time_after_model_creation - self.model.time_start)
        mod_creation_s = time_model_creation.total_seconds()

        time_solve = (
            self.model.time_after_solve - self.model.time_after_model_creation)
        solve_s = time_solve.total_seconds()

        time_total = self.model.time_after_solve - self.model.time_start
        total_s = time_total.total_seconds()

        # Timings output.
        results += '# timings\n'
        results += ('time_model_creation_seconds: ' + str(mod_creation_s) + 
            '\n')
        results += ('time_solve_seconds: ' + str(solve_s) + '\n')
        results += ('time_total_seconds: ' + str(total_s) + '\n\n') 

        if self.optimal_size == -1:
            results += 'Infeasible'
            return results

        # Optimal matching statistics.
        results += '# optimal matching statistics\n'

        results += 'optimal_size: ' + str(self.optimal_size) + '\n'
        results += ('optimal_maxsizemincost: ' + 
            str(self.optimal_maxsizemincost) + '\n')
        results += ('optimal_maxsizemindegree: ' + 
            str(self.optimal_maxsizemindegree) + '\n')
        results += ('optimal_maxsizeminsqcost: ' + 
            str(self.optimal_maxsizeminsqcost) + '\n')
        results += ('optimal_generousmaxprofile: ' + 
            str(self.model._get_profile_string(
                self.optimal_generousmaxprofile)) + '\n')
        results += ('optimal_greedymaxprofile: ' + 
            str(self.model._get_profile_string(
                self.optimal_greedymaxprofile)) + '\n')
        results += ('optimal_greedyprofile: ' + 
            str(self.model._get_profile_string(
                self.optimal_greedyprofile)) + '\n')
        results += ('optimal_max_lec_abs_diff: ' + 
            str(self.optimal_max_lec_abs_diff) + '\n')
        results += ('optimal_sum_lec_abs_diff: ' + 
            str(self.optimal_sum_lec_abs_diff) + '\n\n')

        return results


    def moregen(self, profile1, profile2):
        """Compares two profiles returning whether the first is more generous.

        Returns:
          Whether the first profile is more generous than the second.
        """
        for i in range(len(profile1) - 1, -1, -1):
            if profile1[i] < profile2[i]:
                return True
            elif profile1[i] > profile2[i]:
                return False
        return False


    def moregre(self, profile1, profile2):
        """Compares two profiles returning whether the first is more greedy.

        Returns:
          Whether the first profile is more greedy than the second.
        """
        for i in range(len(profile1)):
            if profile1[i] > profile2[i]:
                return True
            elif profile1[i] < profile2[i]:
                return False
        return False


    def get_matching_pairs(self, matching):
        """Returns the matched Pair objects.

        Returns:
          The matched Pair objects.
        """
        pairs = self.model.pairs
        matching_pairs = []
        for i in range(self.model.num_students):
            matched_proj = matching[i]
            if not matched_proj == 0:
                pairs_row = pairs[i]

                found = False
                j = 0
                pair = None
                while not found and j < len(pairs_row):
                    if pairs_row[j].projectID == matched_proj:
                        pair = pairs_row[j]
                        found = True
                    j += 1

                matching_pairs.append(pair)

        return matching_pairs


    def is_valid(self, matching_pairs):
        """Returns whether the matching is a valid matching.

        Returns:
          Whether the matching is a valid matching.
        """
        for pair in matching_pairs:
            if pair == None:
                return False

        st_num_allocations = [0] * self.model.num_students
        proj_num_allocations = [0] * self.model.num_projects
        lec_num_allocations = [0] * self.model.num_lecturers
        for pair in matching_pairs:
            st_num_allocations[pair.student_index] += 1
            proj_num_allocations[pair.project_index] += 1
            lec_num_allocations[pair.lecturer_index] += 1

        for st_index in range(self.model.num_students):
            if (st_num_allocations[st_index] > 1):
                return False

        for proj_index in range(self.model.num_projects):
            if not self.instance_options[Instance_options.PC]:
                if (self.model.proj_lower_quotas[proj_index] > 
                    proj_num_allocations[proj_index] or
                    self.model.proj_upper_quotas[proj_index] < 
                    proj_num_allocations[proj_index]):
                    return False
            else:
                if ((self.model.proj_lower_quotas[proj_index] > 
                    proj_num_allocations[proj_index] and
                    not proj_num_allocations[proj_index] == 0) or
                    self.model.proj_upper_quotas[proj_index] < 
                    proj_num_allocations[proj_index]  and
                    not proj_num_allocations[proj_index] == 0):
                    return False

        for lec_index in range(self.model.num_lecturers):
            if (self.model.lec_lower_quotas[lec_index] > 
                lec_num_allocations[lec_index] or
                self.model.lec_upper_quotas[lec_index] < 
                lec_num_allocations[lec_index]):
                return False
        return True
