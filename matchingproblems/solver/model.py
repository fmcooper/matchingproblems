from .enums import *

from pulp import *

"""Model and Pair classes representing an instance of SPA-STL.

SPA-STL is the Student-Project Allocation problem with lecturer preferences over
Students including Ties and Lecturer targets.
"""

class Model:
    """Model representing an SPA-STL instance.

    Attributes:
        num_students: Number of students in the instance.
        num_projects: Number of projects in the instance.
        num_lecturers: Number of lecturers in the instance.
        proj_lower_quotas: List of lower quotas for projects.
        proj_upper_quotas: List of upper quotas for projects.
        lec_lower_quotas: List of lower quotas for lecturers.
        lec_targets: List of lecturer targets.
        lec_upper_quotas: List of upper quotas for lecturers.
        time_start: Start time of this run.
        time_after_model_creation: Time after model is created.
        time_after_solve: Time after solve is completed.
        pairs: The main pairs data structure mirroring the student preference 
          lists. pairs[i][j] represents the student-project pairing at position
          j on student s_i's list.
        project_lists: All student-project pairs associated with each project.
        lecturer_lists: All student-project pairs associated with each lecturer.
        rank_lists: All student-project pairs indexed by student rank.
        lec_overload: List of LpVariables associated with lecturers. For a 
          lecturer, their lec_overload = number of allocations - target.
        lec_underload: List of LpVariables associated with lecturers. For a 
          lecturer, their lec_underload = target - number of allocations.
        abs_lec_diff: List of LpVariables, each element represents the maximum 
          of the associated lec_overload and lec_underload variables.
        project_closures: List of LpVariables associated with project closure
          constraints.
        info_string: String containing constraint and optimisation information.
        pulp_status: Status of the Pulp solver after the latest optimisation.
        OPTIMAL_PULP_STATUS: The optimal status of the Pulp solver.
        time_limit: User defined time limit in seconds.
    """

    def __init__(self):
        """Constructor for the Model."""
        self.num_students = -1
        self.num_projects = -1
        self.num_lecturers = -1

        self.proj_lower_quotas = []
        self.proj_upper_quotas = []
        self.lec_lower_quotas = []
        self.lec_targets = []
        self.lec_upper_quotas = []
        self.proj_lecturers = []
        
        self.pairs = []

        self.info_string = ''
        self.pulp_status = ''
        self.time_limit = None

        self.OPTIMAL_PULP_STATUS = 'Optimal'
        self.NOTSOLVED_PULP_STATUS = 'Not Solved'


    def set_project_lists(self):
        """Sets the project lists from the main pairs data structure."""
        self.project_lists = [[] for i in range(self.num_projects)]
        for st_pairs in self.pairs:
            for st_pr_pair in st_pairs:
                self.project_lists[st_pr_pair.project_index].append(st_pr_pair)


    def set_lecturer_lists(self):
        """Sets the lecturer lists from the main pairs data structure."""
        self.lecturer_lists = [[] for i in range(self.num_lecturers)]
        for st_pairs in self.pairs:
            for st_pr_pair in st_pairs:
                (self.lecturer_lists[st_pr_pair.lecturer_index]
                    .append(st_pr_pair))
  

    def set_rank_lists(self):
        """Sets the student rank lists from the main pairs data structure."""
        self.rank_lists = [[] for i in range(self._get_max_rank())]
        for st_pairs in self.pairs:
            for st_pr_pair in st_pairs:
                self.rank_lists[st_pr_pair.rank_student - 1].append(st_pr_pair)


    def _get_max_rank(self):
        """Returns the maximum rank of any project among all students.

        Returns:
            The maximum integer rank of any project among all students.
        """
        max_rank = 0
        for st_pairs in self.pairs:
            for st_pr_pair in st_pairs:
                if st_pr_pair.rank_student > max_rank:
                    max_rank = st_pr_pair.rank_student
        return max_rank


    def get_max_lec_upper_quota(self):
        """Returns the maximum lecturer upper quota.

        Returns:
            The maximum lecturer upper quota among all lecturers.
        """
        return max(self.lec_upper_quotas)


    def pulp_setup(
        self, prob, instance_options, extra_constraints, optimisation_options):
        """Sets up the required Pulp variables.

        Sets up all necessary Pulp variables according to user chosen options.

        Args:
            prob: Main Pulp LpProblem.
            instance_options: User chosen instance options.
            extra_constraints: User chosen extra constraint options.
            optimisation_options: User chosen optimisation options.
        """

        # set up the main decision variables in the pairs data structure
        for pairs_row in self.pairs:
            for pair in pairs_row:
                pair.pulp_setup(
                    prob, 
                    extra_constraints[Extra_constraints.STAB])

        # set up the load balancing variables if required
        if any(x in optimisation_options for x in [
            Optimisation_options.LOADMAXBAL, 
            Optimisation_options.LOADSUMBAL]):

            self.lec_overload = []
            self.lec_underload = []
            self.abs_lec_diff = []

            for lec_index in range(self.num_lecturers):
                lec_upper_quota = self.lec_upper_quotas[lec_index]
                lec_upper_quota_neg = -1 * lec_upper_quota

                # lecturer overload variable
                over_var = LpVariable(
                    "lec_overload_{}".format(lec_index), 
                    lowBound = lec_upper_quota_neg, 
                    upBound = lec_upper_quota, 
                    cat = "Integer")
                self.lec_overload.append(over_var)

                # lecturer underload variable
                under_var = LpVariable(
                    "lec_underload_{}".format(lec_index), 
                    lowBound = lec_upper_quota_neg, 
                    upBound = lec_upper_quota, 
                    cat = "Integer")
                self.lec_underload.append(under_var)

                # absolute lecturer differences
                abs_lec_diff_var = LpVariable(
                    "abs_lec_diff_{}".format(lec_index), 
                    lowBound = 0, 
                    upBound = lec_upper_quota, 
                    cat = "Integer")
                self.abs_lec_diff.append(abs_lec_diff_var)

        # set up project closure variables if required
        if instance_options[Instance_options.PC]:
            self.project_closures = []
            for proj_index in range(self.num_projects):
                proj_closures_var = LpVariable(
                    "project_closures_{}".format(proj_index), cat="Binary")
                self.project_closures.append(proj_closures_var)


    def get_debug(self):
        """Returns Pair variable information.

        Returns:
          Pair variable information.
        """
        lp_vars_string = 'Main lp decision variables:\n'
        for pair_row in self.pairs:
            for pair in pair_row:
                if (pair.lp_var.varValue > 0.9):
                    lp_vars_string += '1 '
                else:
                    lp_vars_string += '0 '
            lp_vars_string += '\n'
        lp_vars_string += '\n'

        lp_vars_string += 'Project closure variables:\n'
        for var in self.project_closures:
            if (var.varValue > 0.9):
                lp_vars_string += '1 '
            else:
                lp_vars_string += '0 '
            
        lp_vars_string += '\n'

        model_information = 'Model instance information:\n'
        model_information += self._pairs_string(self.pairs)

        return lp_vars_string + '\n' + model_information 


    def _pairs_string(self, pairs):
        """Returns a string representation of a variable 2D list of Pairs.

        Args:
          A variable 2D list of Pairs.

        Returns:
          String representation of a variable 2D list of Pairs.
        """
        pairs_string = ''
        for pairs_row in pairs:
            for pair in pairs_row:
                pairs_string += str(pair) + ' '
            pairs_string += '\n'
        return pairs_string
    

    def get_results(self, short_or_long, stable_correctness=False):
        """Returns a string containing the results of the run.

        Args:
          short_or_long: An enum indicating if the results should be long or 
            short.

        Returns:
          String output results for the run.
        """

        # Header.
        start_time_string = self.time_start.strftime("%d %b %Y, %X %Z")
        results = ('# Results for the run conducted on ' 
            + start_time_string + '\n\n')

        # Constraints and optimisations.
        results += '# main constraints and optimisations\n'
        results += self.info_string + '\n'

        # Timings calculations.
        time_model_creation = self.time_after_model_creation - self.time_start
        mod_creation_s = time_model_creation.total_seconds()

        time_solve = self.time_after_solve - self.time_after_model_creation
        solve_s = time_solve.total_seconds()

        time_total = self.time_after_solve - self.time_start
        total_s = time_total.total_seconds()

        # Timeout output.
        if not self.time_limit == None:
            if self.pulp_status == self.NOTSOLVED_PULP_STATUS or total_s > self.time_limit: 
                results += 'Timeout: ' + str(self.time_limit) + ' seconds\n'
                return results

        # Solver status.
        results += '# solver status\n'
        results += 'pulp_status: ' + self.pulp_status + '\n\n'
        if not self.pulp_status == self.OPTIMAL_PULP_STATUS: 
            return results

        # Timings output.
        results += '# timings\n'
        results += ('time_model_creation_seconds: ' + str(mod_creation_s) + 
            '\n')
        results += ('time_solve_seconds: ' + str(solve_s) + '\n')
        results += ('time_total_seconds: ' + str(total_s) + '\n\n')  

        # Stability correctness.
        if stable_correctness:
            pair_assignments_with_None = self._get_pair_assignments_with_none()
            results += ('stability_correct: ' + str(self.check_stability(pair_assignments_with_None)) + '\n\n')

        # Matching statistics output.
        pair_assignments = self._get_pair_assignments()
        results += '# matching statistics\n'
        if short_or_long == Output_type.LONG:
            results += '# the projects assigned to each student\n'
        results += ('matching: ' + self._get_matching_string(pair_assignments) +
            '\n')
        if short_or_long == Output_type.LONG:
            results += '# the sum of ranks of matched students\n'
        results += 'cost: ' + str(self._get_cost(pair_assignments)) + '\n'
        if short_or_long == Output_type.LONG:
            results += '# the sum of squares of ranks of matched students\n'
        results += ('cost_sq: ' + str(self._get_cost_sq(pair_assignments)) + 
            '\n')
        if short_or_long == Output_type.LONG:
            results += '# the highest rank of a matched student\n'
        results += 'degree: ' + str(self._get_degree(pair_assignments)) + '\n'   
        if short_or_long == Output_type.LONG:
            results += '# the number of students gaining their 1st, 2nd, 3rd\n' 
            results += '# choice project etc\n'
        results += ('profile: ' + self._get_profile_string(self._get_profile(pair_assignments)) + 
            '\n')
        if short_or_long == Output_type.LONG:
            results += '# the maximum absolute difference between a \n'
            results += '# lecturer\'s number of allocations and their target\n'
        results += ('max_lec_abs_diff: ' + 
            str(self._get_max_lec_abs_diff(pair_assignments)) + '\n')
        if short_or_long == Output_type.LONG:
            results += '# the sum of differences between a lecturer\'s \n'
            results += '# number of allocations and their target\n'
        results += ('sum_lec_abs_diff: ' + 
            str(self._get_sum_lec_abs_diff(pair_assignments)) + '\n\n')

        # Detailed student, project and lecturer information.
        if short_or_long == Output_type.LONG:
            results += '# details of which project each student is assigned\n'
            results += 'Student_assignments:\n'
            results += self._get_detailed_student_info(pair_assignments) + '\n'

            results += '# details of which students each project is assigned,\n'
            results += '# and the number of students assigned compared to the\n' 
            results += '# projects maximum capacity\n' 
            results += 'Project_assignments:\n'
            results += self._get_detailed_project_info(pair_assignments) + '\n'

            results += '# details of which students each lecturer is\n'
            results += '# assigned, and the number of students assigned\n' 
            results += '# compared to the lecturers maximum capacity (target\n'
            results += '# in brackets)\n' 
            results += 'Lecturer_assignments:\n'
            results += self._get_detailed_lecturer_info(pair_assignments)

        return results


    def _get_pair_assignments(self):
        """Returns the matched Pairs of the matching.

        Returns:
          The matched Pairs of the matching.
        """

        pair_assignments = []
        for pair_row in self.pairs:
            for pair in pair_row:
                if pair.lp_var.varValue:
                    pair_assignments.append(pair)
        return pair_assignments


    def _get_pair_assignments_with_none(self):
        """Returns the Pairs of the matching for each student.

        If a student is not assigned, the entry is None.

        Returns:
          The Pairs of the matching for each student.
        """

        pair_assignments = []
        for pair_row in self.pairs:
            added = False
            for pair in pair_row:
                if pair.lp_var.varValue:
                    pair_assignments.append(pair)
                    added = True
            if not added:
                pair_assignments.append(None)
        return pair_assignments


    def _get_matching_string(self, pair_assignments):
        """Returns a string containing the student-project assignments.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          The student-project assignments.
        """

        matching = ['0'] * self.num_students
        for pair in pair_assignments:
            matching[pair.student_index] = str(pair.projectID)
        return ' '.join(matching)


    def _get_cost(self, pair_assignments):
        """Returns the sum of student ranks for the matching.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          The sum of student ranks for the matching.
        """

        cost = 0
        for pair in pair_assignments:
            cost += pair.rank_student
        return cost


    def _get_cost_sq(self, pair_assignments):
        """Returns the sum of squares of student ranks for the matching.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          The sum of squares of student ranks for the matching.
        """

        cost_sq = 0
        for pair in pair_assignments:
            cost_sq += pair.rank_student * pair.rank_student
        return cost_sq


    def _get_degree(self, pair_assignments):
        """Returns a the degree of the matching as a String.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          The degree of the matching.
        """

        max_matched_rank = 0
        for pair in pair_assignments:
            if pair.rank_student > max_matched_rank:
                max_matched_rank = pair.rank_student
        return max_matched_rank


    def _get_profile_string(self, rank_allocations):
        """Returns a string of the profile of the matching.

        The profile of a matching indicates the number of 1st, 2nd, 3rd... 
        choices etc.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          The profile of the matching as a string.
        """

        profile_string = '< '
        for num_alloc in rank_allocations:
            profile_string += str(num_alloc) + ' '
        profile_string += '>'
        return profile_string




    def _get_profile(self, pair_assignments):
        """Returns the profile of the matching.

        The profile of a matching indicates the number of 1st, 2nd, 3rd... 
        choices etc.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          The profile of the matching.
        """

        max_rank = self._get_max_rank()
        rank_allocations = [0] * max_rank
        for pair in pair_assignments:
            rank_allocations[pair.rank_student - 1] += 1
        return rank_allocations


    def _get_max_lec_abs_diff(self, pair_assignments):
        """Returns the maximum lecturer absolute difference.

        The maximum lecturer absolute difference is the maximum difference
        between a lecturer's number of allocations and their target, over all 
        lecturers.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          The maximum lecturer absolute difference of the matching.
        """

        lec_abs_diffs = self._get_lec_abs_diffs(pair_assignments)
        max_lec_abs_diff = 0
        for abs_diff in lec_abs_diffs:
            if abs_diff > max_lec_abs_diff:
                max_lec_abs_diff = abs_diff
        return max_lec_abs_diff


    def _get_sum_lec_abs_diff(self, pair_assignments):
        """Returns a string containing the sum of lecturer absolute differences.

        The sum of lecturer absolute differences is the sum of differences
        between a lecturer's number of allocations and their target.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          The sum of lecturer absolute differences of the matching.
        """

        lec_abs_diffs = self._get_lec_abs_diffs(pair_assignments)
        sum_lec_abs_diff = 0
        for abs_diff in lec_abs_diffs:
            sum_lec_abs_diff += abs_diff
        return sum_lec_abs_diff


    def _get_lec_abs_diffs(self, pair_assignments):
        """Returns the lecturer absolute differences.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          The lecturer absolute differences.
        """

        # get number of lecturer allocations
        lec_num_allocations = [0] * self.num_lecturers
        for pair in pair_assignments:
            lec_num_allocations[pair.lecturer_index] += 1

        # get absolute difference of lecturer allocations and targets
        lec_abs_diffs = [0] * self.num_lecturers
        for lec_index in range(self.num_lecturers):
            lpos = lec_num_allocations[lec_index] - self.lec_targets[lec_index]
            lneg = self.lec_targets[lec_index] - lec_num_allocations[lec_index]
            if lpos > lneg:
                lec_abs_diffs[lec_index] = lpos
            else:
                lec_abs_diffs[lec_index] = lneg

        return lec_abs_diffs


    def _get_detailed_student_info(self, pair_assignments):
        """Returns a string containing detailed student matching output.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          Detailed student matching output.
        """

        st_lines = [''] * self.num_students
        for pair in pair_assignments:
            st_lines[pair.student_index] = ('s_' + str(pair.studentID) + 
                ': p_' + str(pair.projectID) + ' (l_' + str(pair.lecturerID) + 
                ') \n')

        for i, entry in enumerate(st_lines):
            if entry == '':
                st_lines[i] = ('s_' + str(i + 1) + ' no assignment\n')
        return ''.join(st_lines)


    def _get_detailed_project_info(self, pair_assignments):
        """Returns a string containing detailed project matching output.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          Detailed project matching output.
        """

        p_assignments = [''] * self.num_projects
        p_num_assignments = [0] * self.num_projects
        for pair in pair_assignments:
            p_assignments[pair.project_index] += ('s_' + str(pair.studentID) + 
                ' ')
            p_num_assignments[pair.project_index] += 1

        pr_lines = [''] * self.num_projects

        for j, entry in enumerate(p_assignments):
            pr_lines[j] += ('p_' + str(j + 1) + ' (l_' + 
                str(self.proj_lecturers[j]) + '): ')

            if entry == '':
                pr_lines[j] += 'no assignment '
            else:
                pr_lines[j] += entry

            pr_lines[j] += '    ' + (str(p_num_assignments[j]) + '/' + 
                str(self.proj_upper_quotas[j]) + '\n')
        return ''.join(pr_lines)


    def _get_detailed_lecturer_info(self, pair_assignments):
        """Returns a string containing detailed lecturer matching output.

        Args:
          pair_assignments: List of student-project matched Pairs.

        Returns:
          Detailed lecturer matching output.
        """

        l_assignments = [''] * self.num_lecturers
        l_num_assignments = [0] * self.num_lecturers
        for pair in pair_assignments:
            l_assignments[pair.lecturer_index] += ('s_' + str(pair.studentID) + 
                ' (' + 'p_' + str(pair.projectID) + ') ')
            l_num_assignments[pair.lecturer_index] += 1

        lec_lines = [''] * self.num_lecturers

        for k, entry in enumerate(l_assignments):
            lec_lines[k] += ('l_' + str(k + 1) + ': ')

            if entry == '':
                lec_lines[k] += 'no assignment '
            else:
                lec_lines[k] += entry

            lec_lines[k] += '    ' + (str(l_num_assignments[k]) + '/' + 
                str(self.lec_upper_quotas[k]) + ' (' + 
                str(self.lec_targets[k]) + ')\n')
        return ''.join(lec_lines)


    def check_stability(self, pair_assignments_with_none):
        """Checks whether a matching is stable.

        Args:
          pair_assignments_with_none: List of student-project Pairs.

        Returns:
          Whether the current matching is stable.
        """

        p_num_assignments = self.get_num_assignments_projects(pair_assignments_with_none)
        l_num_assignments = self.get_num_assignments_lecturers(pair_assignments_with_none)
        worst_rank_projects = self.get_worst_rank_projects(pair_assignments_with_none)
        worst_rank_lecturers = self.get_worst_rank_lecturers(pair_assignments_with_none)

        # Iterate over the student preference list checking if the student
        # would like to move.
        for i, pair_row in enumerate(self.pairs):
            assigned_pair_i = pair_assignments_with_none[i]
            for pair in pair_row:
                # See stability definition page 22 of http://theses.gla.ac.uk/81622/
                blocking_pair_2 = False
                blocking_pair_3a = False
                blocking_pair_3b = False
                blocking_pair_3c = False

                # blocking_pair_2
                if assigned_pair_i == None:
                    blocking_pair_2 = True
                elif pair.rank_student < assigned_pair_i.rank_student:
                    blocking_pair_2 = True

                # blocking_pair_3a
                p_undersubscribed = p_num_assignments[pair.project_index] < self.proj_upper_quotas[pair.project_index]
                l_undersubscribed = l_num_assignments[pair.lecturer_index] < self.lec_upper_quotas[pair.lecturer_index]
                if (p_undersubscribed and l_undersubscribed):
                    blocking_pair_3a = True

                # blocking_pair_3b
                if (p_undersubscribed and not l_undersubscribed and 
                    ((not assigned_pair_i == None and assigned_pair_i.lecturer_index == pair.lecturer_index) or
                        pair.rank_lecturer < worst_rank_lecturers[pair.lecturer_index])):
                    blocking_pair_3b = True

                # blocking_pair_3c
                if (not p_undersubscribed and 
                    pair.rank_lecturer < worst_rank_projects[pair.project_index]):
                    blocking_pair_3c = True

                blocking_pair = blocking_pair_2 and (blocking_pair_3a or blocking_pair_3b or blocking_pair_3c)
                if blocking_pair:
                    return False
        return True


    def get_num_assignments_projects(self, pair_assignments_with_none):
        """Returns the number of assignments for each project.

        Args:
          pair_assignments_with_none: List of student-project Pairs.

        Returns:
          The number of assignments for each project.
        """
        num_assignments = [0] * self.num_projects
        for pair in pair_assignments_with_none:
            if not pair == None:
                num_assignments[pair.project_index] += 1
        return num_assignments


    def get_num_assignments_lecturers(self, pair_assignments_with_none):
        """Returns the number of assignments for each lecturer.

        Args:
          pair_assignments_with_none: List of student-project Pairs.

        Returns:
          The number of assignments for each lecturer.
        """
        num_assignments = [0] * self.num_lecturers
        for pair in pair_assignments_with_none:
            if not pair == None:
                num_assignments[pair.lecturer_index] += 1
        return num_assignments


    def get_worst_rank_projects(self, pair_assignments_with_none):
        """Returns the worst rank of the worst student assigned to each project.

        Args:
          pair_assignments_with_none: List of student-project Pairs.

        Returns:
          The worst rank of the worst student assigned to each project.
        """
        worst_ranks = [None] * self.num_projects
        for pair in pair_assignments_with_none:
            if not pair == None:
                if worst_ranks[pair.project_index] == None:
                    worst_ranks[pair.project_index] = pair.rank_lecturer
                elif pair.rank_lecturer > worst_ranks[pair.project_index]:
                    worst_ranks[pair.project_index] = pair.rank_lecturer
        return worst_ranks


    def get_worst_rank_lecturers(self, pair_assignments_with_none):
        """Returns the worst rank of the worst student assigned to each lecturer.

        Args:
          pair_assignments_with_none: List of student-project Pairs.

        Returns:
          The worst rank of the worst student assigned to each lecturer.
        """
        worst_ranks = [None] * self.num_lecturers
        for pair in pair_assignments_with_none:
            if not pair == None:
                if worst_ranks[pair.lecturer_index] == None:
                    worst_ranks[pair.lecturer_index] = pair.rank_lecturer
                elif pair.rank_lecturer > worst_ranks[pair.lecturer_index]:
                    worst_ranks[pair.lecturer_index] = pair.rank_lecturer
        return worst_ranks


class Pair:
    """Student-Project Pair.

    Represents a student-project pairing on a student's preference list.

    Attributes:
        studentID: ID number for the associated student (integer >= 1).
        projectID: ID number for the associated project (integer >= 1).
        lecturerID: ID number for the associated lecturer (integer >= 1).
        student_index: Index of the associated student (integer >= 0).
        project_index: Index of the associated project (integer >= 0).
        lecturer_index: Index of the associated lecturer (integer >= 0).
        rank_student: Rank of this project for this student (integer >= 1).
        rank_lecturer: Rank of this student for this lecturer (integer >= 1).
        lp_var: = 1 if this student is assigned to this project (LpVariable).
        alpha_var: Used in stability constraints (LpVariable).
        beta_var: Used in stability constraints (LpVariable).
    """

    def __init__(self, studentID, projectID, rank_student):
        """Initialises Pair with student and project information.

        Args:
            studentID: ID number for the associated student.
            projectID: ID number for the associated project.
            rank_student: Rank of this project for this student.
        """
        self.studentID = studentID
        self.projectID = projectID
        self.student_index = self.studentID - 1
        self.project_index = self.projectID - 1
        self.rank_student = rank_student


    def set_lecturer(self, lecturerID):
        """Sets the lecturer ID and index.

        Args:
            lecturerID: ID number for the associated lecturer.
        """
        self.lecturerID = lecturerID
        self.lecturer_index = self.lecturerID - 1

    
    def set_lecturer_rank(self, rank):
        """Sets the lecturer ID and index.

        Args:
            rank: Rank of the student of this Pair for this lecturer.
        """
        self.rank_lecturer = rank
            
        
    def pulp_setup(self, prob, alphabeta):
        """Sets up the Pulp variables for this Pair.

        Args:
            prob: Main Pulp LpProblem.
            alphabeta: Boolean indicator, defining whether alpha and beta 
              variables need to be set up for stability constraints.
        """
        var_name = '(' + str(self.studentID) + ',' + str(self.projectID) + ')'
        self.lp_var = LpVariable(var_name, cat='Binary')

        if alphabeta:
            var_name_alpha = ('a' + var_name)
            self.alpha_var = LpVariable(var_name_alpha, cat='Binary')
            var_name_beta = ('b' + var_name)
            self.beta_var = LpVariable(var_name_beta, cat='Binary')


    def __str__(self):
        """String representation of this Pair."""
        return ('(s' + str(self.studentID) + ' p' + str(self.projectID) + 
            ' rs' + str(self.rank_student) + ' l' + str(self.lecturerID) + 
            ' rl' + str(self.rank_lecturer) + ')')
