import matchingproblems
from matchingproblems.generator import instance_options_parser as iop
import unittest

"""Testing class for Instance options parser."""

class TestParser(unittest.TestCase):

    def test_inputs_required_hr(self):
        required_input_examples = [
            '-numinst 3',
            '-o ./out',
            '-mp hr',
            '-n1 6',
            '-n2 4',
            '-pmin 2',
            '-pmax 4',
            '-uq 6',
            '-pl2',
            ]
        for i, inexample in enumerate(required_input_examples):
            with self.subTest(i=i):
                input_list = required_input_examples.copy()
                input_list.pop(i)
                input_args = ' '.join(input_list).split()
                print(input_args)
                parser = iop.Instance_options_parser()
                with self.assertRaises(SystemExit):
                    parser.parse(input_args)

    def test_inputs_banned_hr(self):
        good_input = '-numinst 3 -o ./out -mp hr -pl2 -n1 6 -n2 4 -pmin 2 -pmax 4 -uq 6'
        banned_input_examples = [
            '-n3 3',
            '-llq 0',
            '-luq 6',
            '-lt 3',
            ]
        for i, inexample in enumerate(banned_input_examples):
            with self.subTest(i=i):
                input_args = (good_input + ' ' + inexample).split()
                print(input_args)
                parser = iop.Instance_options_parser()
                with self.assertRaises(SystemExit):
                    parser.parse(input_args)


    def test_inputs_required_ha(self):
        required_input_examples = [
            '-numinst 3',
            '-o ./out',
            '-mp ha',
            '-n1 6',
            '-n2 4',
            '-pmin 2',
            '-pmax 4',
            '-uq 6',
            ]
        for i, inexample in enumerate(required_input_examples):
            with self.subTest(i=i):
                input_list = required_input_examples.copy()
                input_list.pop(i)
                input_args = ' '.join(input_list).split()
                print(input_args)
                parser = iop.Instance_options_parser()
                with self.assertRaises(SystemExit):
                    parser.parse(input_args)


    def test_inputs_banned_ha(self):
        good_input = '-numinst 3 -o ./out -mp ha -n1 6 -n2 4 -pmin 2 -pmax 4 -uq 6'
        banned_input_examples = [
            '-pl2',
            '-n3 3',
            '-t2 0.2',
            '-llq 0',
            '-luq 6',
            '-lt 3',
            ]
        for i, inexample in enumerate(banned_input_examples):
            with self.subTest(i=i):
                input_args = (good_input + ' ' + inexample).split()
                print(input_args)
                parser = iop.Instance_options_parser()
                with self.assertRaises(SystemExit):
                    parser.parse(input_args)


    def test_inputs_required_sm(self):
        required_input_examples = [
            '-numinst 3',
            '-o ./out',
            '-mp sm',
            '-n1 6',
            '-pmin 2',
            '-pmax 4',
            '-pl2',
            ]
        for i, inexample in enumerate(required_input_examples):
            with self.subTest(i=i):
                input_list = required_input_examples.copy()
                input_list.pop(i)
                input_args = ' '.join(input_list).split()
                print(input_args)
                parser = iop.Instance_options_parser()
                with self.assertRaises(SystemExit):
                    parser.parse(input_args)


    def test_inputs_banned_sm(self):
        good_input = '-numinst 3 -o ./out -mp sm -n1 6 -n2 4 -pmin 2 -pmax 4 -uq 6'
        banned_input_examples = [
            '-n2 4',
            '-n3 3',
            '-t2 0.2',
            '-uq 6',
            '-lq 1',
            '-llq 0',
            '-luq 6',
            '-lt 3',
            ]
        for i, inexample in enumerate(banned_input_examples):
            with self.subTest(i=i):
                input_args = (good_input + ' ' + inexample).split()
                print(input_args)
                parser = iop.Instance_options_parser()
                with self.assertRaises(SystemExit):
                    parser.parse(input_args)

    def test_inputs_required_spa(self):
        required_input_examples = [
            '-numinst 3',
            '-o ./out',
            '-mp spa',
            '-n1 6',
            '-n2 4',
            '-n3 3',
            '-pmin 2',
            '-pmax 4',
            '-llq 0',
            '-luq 6',
            '-lt 3',
            ]
        for i, inexample in enumerate(required_input_examples):
            with self.subTest(i=i):
                input_list = required_input_examples.copy()
                input_list.pop(i)
                input_args = ' '.join(input_list).split()
                print(input_args)
                parser = iop.Instance_options_parser()
                with self.assertRaises(SystemExit):
                    parser.parse(input_args)
