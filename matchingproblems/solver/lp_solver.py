from .enums import *

from pulp import *

"""IP solver for an instance of SPA-STL.

SPA-STL is the Student-Project Allocation problem with lecturer preferences over
Students including Ties and Lecturer targets.
"""

class LP_Solver:
    """ IP solver for an instance of SPA-STL.

    Attributes:
        model: Model representing an SPA-STL instance.
        prob: Main Pulp LpProblem.
        info_string: String containing constraint and optimisation information.
        instance_options: User chosen instance options.
        extra_constraints: User chosen extra constraint options.
        optimisation_options: User chosen optimisation options.
        solver: The Pulp solver.
    """
    def __init__(
        self, 
        model, 
        instance_options, 
        extra_constraints, 
        optimisation_options):
        """Constructor for the Solver.

        Args:
            model: Model representing an SPA-STL instance. 
            instance_options: User chosen instance options.
            extra_constraints: User chosen extra constraint options.
            optimisation_options: User chosen optimisation options.
        """

        self.model = model
        self.instance_options = instance_options
        self.extra_constraints = extra_constraints
        self.optimisation_options = optimisation_options

        # Set up the Pulp Lp problem.
        self.prob = LpProblem("Student-Project-Allocator", LpMaximize)
        self.prob += 0, "Arbitrary Objective Function"
        self.model.pulp_setup(
            self.prob, 
            self.instance_options, 
            self.extra_constraints, 
            self.optimisation_options)
        

    def run(self, msg, timeLimit, threads, write):
        """Run the solver.

        Args:
          msg: Pulp indicator as to whether the solver should output info.
          timeLimit: Pulp time limit for optimisations (note this will be for 
            each individual optimisation, exceeding the overall time limit will
            be dealt with in another part of the program).
          threads: Pulp variable for the number of threads to use when solving.
          write: Indicates whether the model should be written to file.

        Return:
          The most recent Pulp solver status (either Optimal, or the first non
           Optimal status).
        """

        self.info_string = ''
        self.solver = pulp.PULP_CBC_CMD(
            msg=msg, 
            timeLimit=timeLimit, 
            threads=threads)

        self.add_constraints(
            self.instance_options, 
            self.extra_constraints, 
            self.optimisation_options)

        self.run_optimisations(self.optimisation_options)

        if len(self.optimisation_options) == 0:
            self.prob.solve(self.solver)

        self.model.info_string = self.info_string
        if write:
            self.prob.writeLP('model.lp')
        return LpStatus[self.prob.status] 

    
    def add_constraints(
        self, instance_options, extra_constraints, optimisation_options):
        """Add all required constraints to the Lp model.

        Args:
            instance_options: User chosen instance options.
            extra_constraints: User chosen extra constraint options.
            optimisation_options: User chosen optimisation options.
        """

        # Add basic matching constraints.
        self.upper_lower_constraints(instance_options)

        # Add stability constraints if required.
        if extra_constraints[Extra_constraints.STAB]:
            self.stability_constraints()

        # Add load balancing constraints if required.
        if any(x in optimisation_options for x in [
            Optimisation_options.LOADMAXBAL, 
            Optimisation_options.LOADSUMBAL]):
            self.loadbalancing_constraints()



    def upper_lower_constraints(self, instance_options):
        """Add basic matching constraints.

        Args:
            instance_options: User chosen instance options.
        """

        self.info_string += '- valid matching constraints added\n'

        # Each student must be assigned either 0 or 1 projects.
        for st_index, pairs_row in enumerate(self.model.pairs):
            self.prob += (
                lpSum([pair.lp_var for pair in pairs_row]) <= 1, 
                "st_limit_{}".format(st_index))
            
        # Upper and lower quota constraints on projects.
        if instance_options[Instance_options.PC]:
            self.info_string += '- project closures allowed\n'
            
        for proj_index, pairs_row in enumerate(self.model.project_lists):
            proj_vars = lpSum([pair.lp_var for pair in pairs_row])
            lq = self.model.proj_lower_quotas[proj_index]
            uq = self.model.proj_upper_quotas[proj_index]

            # If project closures are selected, then the number of students
            # assigned to this project must be greater than (less than) the 
            # lower quota (upper quota) if the project is open, or 0 if the 
            # project is closed. 
            if instance_options[Instance_options.PC]:
                pc_lq_exp = LpAffineExpression(proj_vars)
                pc_lq_exp += self.model.project_closures[proj_index] * lq
                self.prob += (
                    pc_lq_exp >= lq, 
                    "proj_cl_lq_{}".format(proj_index))

                pc_uq_exp = LpAffineExpression(proj_vars)
                pc_uq_exp += self.model.project_closures[proj_index] * uq
                self.prob += (
                    pc_uq_exp <= uq, 
                    "proj_cl_uq_{}".format(proj_index))

            # Otherwise use upper and lower constraints as usual.
            else:
                self.prob += (proj_vars >= lq, "proj_lq_{}".format(proj_index))
                self.prob += (proj_vars <= uq, "proj_uq_{}".format(proj_index))

        # Upper and lower quota constraints on lecturers.
        for lec_index, pairs_row in enumerate(self.model.lecturer_lists):
            self.prob += (
                (lpSum([pair.lp_var for pair in pairs_row]) 
                    >= self.model.lec_lower_quotas[lec_index]), 
                "lec_lq_{}".format(lec_index))
            self.prob += (
                (lpSum([pair.lp_var for pair in pairs_row]) 
                    <= self.model.lec_upper_quotas[lec_index]), 
                "lec_uq_{}".format(lec_index))
            
        
    def stability_constraints(self):
        """Adds stability constraints to model by disallowing blocking pairs."""

        self.info_string += '- stability constraints added\n'

        # for each student-project pair
        for i, pairs_row in enumerate(self.model.pairs):
            st_pref_length = len(pairs_row)
            for j, pair in enumerate(pairs_row):

                # si_wants_to_move_pj_exp = 1 if s_i wants to move to p_j (if 
                # either s_i is unassigned in M or s_i prefers p_j to M(s_i)
                # that is, si_wants_to_move_pj_exp = 1 - (sum of variables at an
                # equal or higher rank in the preference list)
                s_i_wants_to_move_exp = LpAffineExpression(1)
                aim_rank = pair.rank_student
                current_rank = 1
                index = 0

                while current_rank <= aim_rank and index < st_pref_length:
                    s_i_wants_to_move_exp -= pairs_row[index].lp_var
                    index += 1
                    if index < st_pref_length:
                        current_rank = pairs_row[index].rank_student

                # lk_sum_better_equal = d_k IF l_k prefers (or is indifferent
                # to) the worst student in M(l_k) to s_i AND s_i not in M(l_k)
                lk_sum_better_equal_exp = LpAffineExpression()
                
                # pj_sum_better_equal = c_j IF l_k prefers (or is indifferent
                # to) the worst student of p_j to s_i
                pj_sum_better_equal_exp = LpAffineExpression()  

                # rank of s_i on l_k's preference list
                aim_rank = pair.rank_lecturer

                # iterate over l_k's lecturer lists (not preference lists)
                for lec_pair in self.model.lecturer_lists[pair.lecturer_index]:
                    if (lec_pair.rank_lecturer <= aim_rank and 
                        not lec_pair.studentID == pair.studentID):
                        # part of 3b)
                        lk_sum_better_equal_exp += lec_pair.lp_var

                        # part of 3c)
                        if lec_pair.projectID == pair.projectID:
                            pj_sum_better_equal_exp += lec_pair.lp_var


                # alpha = 1 IMPLIES THAT l_k is full and prefers their worst 
                # assignee to s_i or is indifferent between them AND s_i is not 
                # in M(l_k)
                alpha_exp = LpAffineExpression()
                neg_l_uq = -1 * self.model.lec_upper_quotas[pair.lecturer_index]
                alpha_exp += neg_l_uq * pair.alpha_var
                alpha_exp += lk_sum_better_equal_exp
                self.prob += (
                    alpha_exp >= 0, 
                    "alpha_({},{})".format(pair.studentID, pair.projectID))

                # beta = 1 IMPLIES THAT p_j is full and l_k prefers their worst
                # assignee of p_j to s_i or is indifferent between them
                beta_exp = LpAffineExpression()
                neg_p_uq = -1 * self.model.proj_upper_quotas[pair.project_index]
                beta_exp += neg_p_uq * pair.beta_var
                beta_exp += pj_sum_better_equal_exp
                self.prob += (
                    beta_exp >= 0, 
                    "beta_({},{})".format(pair.studentID, pair.projectID))

                # If s_i is unmatched or prefers p_j to M(s_i) then alpha or 
                # beta must equal 1
                gamma_exp = LpAffineExpression(s_i_wants_to_move_exp)
                gamma_exp -= pair.alpha_var
                gamma_exp -= pair.beta_var
                self.prob += (
                    gamma_exp <= 0, 
                    "gamma_({},{})".format(pair.studentID, pair.projectID))


    def loadbalancing_constraints(self):
        '''Adds load-balancing constraints to model.'''

        self.info_string += '- load-balancing constraints added\n'

        for lec_index in range(self.model.num_lecturers):
            this_lec_vars = (
                [x.lp_var for x in self.model.lecturer_lists[lec_index]])
            self.model.lec_overload[lec_index] = (
                lpSum(this_lec_vars) - self.model.lec_targets[lec_index])
            self.model.lec_underload[lec_index] = (
                self.model.lec_targets[lec_index] - lpSum(this_lec_vars))
            self.prob += (self.model.abs_lec_diff[lec_index] >= 
                self.model.lec_overload[lec_index])
            self.prob += (self.model.abs_lec_diff[lec_index] >= 
                self.model.lec_underload[lec_index])
        

    def run_optimisations(self, optimisation_options):
        '''Runs optimisations in the given order.

        Args:
            optimisation_options: User chosen optimisation options.
        '''

        for opt in optimisation_options:
            if opt == Optimisation_options.MAXSIZE:
                self.optimisation_maxsize()
            if opt == Optimisation_options.MINSIZE:
                self.optimisation_minsize()
            if opt == Optimisation_options.GENEROUS:
                self.optimisation_generous()
            if opt == Optimisation_options.GREEDY:
                self.optimisation_greedy()
            if opt == Optimisation_options.MINCOST:
                self.optimisation_mincost()
            if opt == Optimisation_options.MINSQCOST:
                self.optimisation_minsqcost()
            if opt == Optimisation_options.LOADMAXBAL:
                self.optimisation_loadmaxbal()
            if opt == Optimisation_options.LOADSUMBAL:
                self.optimisation_loadsumbal()

            # Exit early if one of the optimisations is not solved.
            if not LpStatus[self.prob.status] == self.model.OPTIMAL_PULP_STATUS:
                return None

    
    def optimisation_maxsize(self):
        '''Maximises size of matching and adds constraint.'''
        
        self.info_string += '- optimisation: maximising size\n'
        obj = LpVariable(
                "obj_maxsize", 
                lowBound = 0, 
                upBound = self.model.num_students, 
                cat = "Integer")
        all_vars = self.get_all_pairs_vars()
        self.prob += (lpSum(all_vars) == obj)
        self.perform_optimisation(obj, Optimisation_type.MAXIMISE)
        

    def optimisation_minsize(self):
        '''Minimises size of matching and adds constraint.'''

        self.info_string += '- optimisation: minimising size\n'
        obj = LpVariable(
                "obj_minsize", 
                lowBound = 0, 
                upBound = self.model.num_students, 
                cat = "Integer")
        all_vars = self.get_all_pairs_vars()
        self.prob += (lpSum(all_vars) == obj)
        self.perform_optimisation(obj, Optimisation_type.MINIMISE)


    def optimisation_generous(self):
        '''Performs generous optimisation and adds constraints.'''

        self.info_string += '- optimisation: generous\n'
        for r in range(len(self.model.rank_lists),0,-1):

            obj = LpVariable(
                    "obj_generous_rank_" + str(r), 
                    lowBound = 0, 
                    upBound = self.model.num_students, 
                    cat = "Integer")
            all_vars = self.get_all_vars_at_rank(r)
            self.prob += (lpSum(all_vars) == obj)
            self.perform_optimisation(obj, Optimisation_type.MINIMISE)


    def optimisation_greedy(self):
        '''Performs greedy optimisation and adds constraints.'''

        self.info_string += '- optimisation: greedy\n'
        for r in range(1, len(self.model.rank_lists) + 1):

            obj = LpVariable(
                    "obj_greedy_rank_" + str(r), 
                    lowBound = 0, 
                    upBound = self.model.num_students, 
                    cat = "Integer")
            all_vars = self.get_all_vars_at_rank(r)
            self.prob += (lpSum(all_vars) == obj)
            self.perform_optimisation(obj, Optimisation_type.MAXIMISE)


    def optimisation_mincost(self):
        '''Minimises sum of ranks of matched students and adds constraint.'''

        self.info_string += '- optimisation: minimising sum of ranks\n'
        obj = LpVariable(
                "obj_mincost", 
                lowBound = 0, 
                upBound = self.model.num_students * len(self.model.rank_lists), 
                cat = "Integer")
        sum_ranks_exp = LpAffineExpression()
        for r in range(1, len(self.model.rank_lists) + 1):
            vars_at_rank = self.get_all_vars_at_rank(r)
            sum_ranks_exp += lpSum(vars_at_rank) * r

        self.prob += (sum_ranks_exp == obj)
        self.perform_optimisation(obj, Optimisation_type.MINIMISE)


    def optimisation_minsqcost(self):
        '''Minimises sum of squares of ranks of matched students and adds 
        constraint.'''

        self.info_string += '- optimisation: minimising sum of square of ranks\n'
        up_bound = self.model.num_students * len(self.model.rank_lists)
        up_bound = up_bound * up_bound
        obj = LpVariable(
                "obj_mincost", 
                lowBound = 0, 
                upBound = up_bound, 
                cat = "Integer")
        sum_ranks_exp = LpAffineExpression()
        for r in range(1, len(self.model.rank_lists) + 1):
            vars_at_rank = self.get_all_vars_at_rank(r)
            sum_ranks_exp += lpSum(vars_at_rank) * r * r

        self.prob += (sum_ranks_exp == obj)
        self.perform_optimisation(obj, Optimisation_type.MINIMISE)


    def optimisation_loadmaxbal(self):
        '''Minimises the load max balanced value and adds constraint.'''

        self.info_string += '- optimisation: load max balanced\n'
        obj = LpVariable(
            "lec_max_abs_diff", 
            lowBound = 0,
            upBound = self.model.get_max_lec_upper_quota(),
            cat="Integer")
        
        for lec_index in range(self.model.num_lecturers):
            self.prob += (obj >= self.model.abs_lec_diff[lec_index])
        self.perform_optimisation(obj, Optimisation_type.MINIMISE)


    def optimisation_loadsumbal(self):
        '''Minimises the load sum balanced value and adds constraint.'''

        self.info_string += '- optimisation: load sum balanced\n'
        obj = LpVariable(
            "lec_sum_abs_diff", 
            lowBound = 0,
            upBound = (self.model.get_max_lec_upper_quota() * 
                self.model.num_students),
            cat="Integer")
        
        self.prob += (obj >= lpSum(self.model.abs_lec_diff))
        self.perform_optimisation(obj, Optimisation_type.MINIMISE)


    def get_all_pairs_vars(self):
        '''Returns all lp_var variables in the main pairs data structure.

        Returns:
            All lp_var variables from the main pairs data structure.
        '''
        
        all_vars = []
        for pairs_row in self.model.pairs:
            for pair in pairs_row:
                all_vars.append(pair.lp_var)
        return all_vars


    def get_all_vars_at_rank(self, r):
        '''Returns all lp_var variables with a given student rank.

        Returns:
            All lp_var variables with a given student rank.
        '''
        all_vars = []
        for pair in self.model.rank_lists[r - 1]:
            all_vars.append(pair.lp_var)
        return all_vars


    def perform_optimisation(self, objective_function, optimisation_type):
        '''Either maximises or minimises the given objective function.
        
        Args: 
            objective_function: The objective function.
            optimisation_type: Enum indicating whether to maximise or minimise.

        '''

        if optimisation_type == Optimisation_type.MAXIMISE:
            self.prob.objective = objective_function
            self.prob.solve(self.solver)
            # add the constraint
            self.prob += objective_function >= objective_function.varValue

        elif optimisation_type == Optimisation_type.MINIMISE:
            self.prob.objective = -1 * objective_function
            self.prob.solve(self.solver)
            # add the constraint
            self.prob += objective_function <= objective_function.varValue
