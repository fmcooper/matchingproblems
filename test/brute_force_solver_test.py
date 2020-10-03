import matchingproblems
from matchingproblems.solver import brute_force_solver, model, enums
import unittest

"""Testing class for the model class."""

class TestModel(unittest.TestCase):

    def create_example_model(self):
        m = model.Model()
        m.num_students = 2
        m.num_projects = 2
        m.num_lecturers = 2
        m.proj_lower_quotas = [0, 1]
        m.proj_upper_quotas = [1, 2]
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


    def test_moregen(self):
        bfs = brute_force_solver.Brute_force_solver(None, model.Model())
        self.assertEqual(bfs.moregen([2, 1], [1, 2]), True)

        self.assertEqual(bfs.moregen([1, 2], [2, 1]), False)


    def test_moregre(self):
        bfs = brute_force_solver.Brute_force_solver(None, model.Model())
        self.assertEqual(bfs.moregre([2, 1], [1, 2]), True)

        self.assertEqual(bfs.moregre([1, 2], [2, 1]), False)


    def test_get_matching_pairs(self):
        m = self.create_example_model()
        bfs = brute_force_solver.Brute_force_solver(None, m)
        answer = [m.pairs[0][0], m.pairs[1][0]]

        self.assertListEqual(bfs.get_matching_pairs([2, 2]), answer)


    def test_is_valid_true(self):
        m = self.create_example_model()
        instance_options = {
                            enums.Instance_options.PC: False,
            }
        bfs = brute_force_solver.Brute_force_solver(instance_options, m)

        pairs = [m.pairs[0][0], m.pairs[1][0]]
        self.assertEqual(bfs.is_valid(pairs), True)

        pairs = [m.pairs[0][0], m.pairs[0][1]]
        self.assertEqual(bfs.is_valid(pairs), False)
