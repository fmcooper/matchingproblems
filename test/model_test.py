import matchingproblems
from matchingproblems.solver import model
import unittest

"""Testing class for the model class."""

class TestModel(unittest.TestCase):

    def create_example_model(self):
        m = model.Model()
        m.num_students = 2
        m.num_projects = 2
        m.num_lecturers = 2
        m.proj_lower_quotas = [1, 0]
        m.proj_upper_quotas = [2, 1]
        m.lec_lower_quotas = [0, 0]
        m.lec_targets = [1, 1]
        m.lec_upper_quotas = [2, 2]
        m.proj_lecturers = [1, 2]
        m.pairs = [
            [model.Pair(1, 2, 1), model.Pair(1, 1, 2)],
            [model.Pair(2, 2, 1),]]
        m.pairs[0][0].set_lecturer(2)
        m.pairs[0][0].set_lecturer_rank(1)
        m.pairs[0][1].set_lecturer(1)
        m.pairs[0][1].set_lecturer_rank(1)
        m.pairs[1][0].set_lecturer(2)
        m.pairs[1][0].set_lecturer_rank(2)
        m.set_project_lists()
        m.set_lecturer_lists()
        m.set_rank_lists()
        return m


    def create_example_pair_assignments(self, m):
        return [m.pairs[0][0], m.pairs[1][0]]


    def test_set_project_lists(self):   
        m = self.create_example_model()
        answer =[
            [m.pairs[0][1]], 
            [m.pairs[0][0], m.pairs[1][0]]]

        self.assertListEqual(m.project_lists, answer)


    def test_set_lecturer_lists(self):   
        m = self.create_example_model()
        answer =[
            [m.pairs[0][1]], 
            [m.pairs[0][0], m.pairs[1][0]]]

        self.assertListEqual(m.lecturer_lists, answer)


    def test_set_set_rank_lists(self):   
        m = self.create_example_model()
        answer =[
            [m.pairs[0][0], m.pairs[1][0]], 
            [m.pairs[0][1]]]

        self.assertListEqual(m.rank_lists, answer)


    def test_get_max_rank(self):   
        m = self.create_example_model()
        self.assertEqual(m._get_max_rank(), 2)


    def test_get_max_lec_upper_quota(self):   
        m = self.create_example_model()
        self.assertEqual(m.get_max_lec_upper_quota(), 2)


    def test_get_matching_string(self):   
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m._get_matching_string(pair_assignments), '2 2')


    def test_get_cost(self):   
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m._get_cost(pair_assignments), 2)


    def test_get_cost_sq(self):   
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m._get_cost_sq(pair_assignments), 2)


    def test_get_degree(self):   
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m._get_degree(pair_assignments), 1)


    def test_get_profile(self):   
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m._get_profile(pair_assignments), [2, 0])


    def test_get_max_lec_abs_diff(self):   
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m._get_max_lec_abs_diff(pair_assignments), 1)


    def test_get_sum_lec_abs_diff(self):   
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m._get_sum_lec_abs_diff(pair_assignments), 2)


    def test_get_lec_abs_diffs(self):
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m._get_lec_abs_diffs(pair_assignments), [1, 1])


    # This function is itself used as a correctness tester so is only briefly 
    # tested here.
    def test_check_stability(self):
        m = self.create_example_model()
        pair_assignments_with_none = self.create_example_pair_assignments(m)
        self.assertEqual(m.check_stability(pair_assignments_with_none), True)


    def test_get_num_assignments_projects(self):
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m.get_num_assignments_projects(pair_assignments), [0, 2])


    def test_get_num_assignments_lecturers(self):
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m.get_num_assignments_projects(pair_assignments), [0, 2])


    def test_get_worst_rank_projects(self):
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m.get_worst_rank_projects(pair_assignments), [None, 2])


    def test_get_worst_rank_lecturers(self):
        m = self.create_example_model()
        pair_assignments = self.create_example_pair_assignments(m)
        self.assertEqual(m.get_worst_rank_lecturers(pair_assignments), [None, 2])
