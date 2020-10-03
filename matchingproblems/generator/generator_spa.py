import argparse
from argparse import RawTextHelpFormatter
from .generator_shared import *
import numpy as np
import os
import random
import sys

"""Generates instances of SPA (and its variants).

This program generate instances of the Student-Project Allocation problem and 
its variants, including lecturer preferences over Students, Ties and lecturer 
Targets. 
"""

class Generator_spa:

    def generate_instances(self, args):
        """Generates an instance of SPA and writes to file.

        Generates and outputs instance of SPA according to user chosen 
        parameters.

        Args:
            args: User chosen instance parameter information.
        """
        if not os.path.exists(args.outputdirectory):
            os.makedirs(args.outputdirectory)

        for instance_number in range(args.numberinstances):
            pref_lists_students, st_ties = create_pref_lists_original(
                args.n1, 
                args.n2, 
                args.minpreflistlength, 
                args.maxpreflistlength, 
                args.ties1, 
                args.skew)  

            project_lecturers = self.create_project_lecturers(args.n2, args.n3)

            # Student lecturer lists are created in order to use the
            # create_pref_lists_from_other_lists function to generate lecturer
            # preferences over students
            st_lec_lists = self.create_student_lec_lists(
                pref_lists_students, project_lecturers, args.n3)

            pref_lists_lecturers, lec_ties = [], []
            if args.twopl:
                pref_lists_lecturers, lec_ties = create_pref_lists_from_other_lists(
                    st_lec_lists, args.n3, args.ties2)

            instance_info = self.create_instance_info(args)

            lower_quotas = create_quotas(args.n2, args.lowerquotas)
            upper_quotas = create_quotas(args.n2, args.upperquotas)
            lec_lower_quotas = create_quotas(args.n3, args.lecturerlowerquotas)
            lec_targets = create_quotas(args.n3, args.lecturertargets)
            lec_upper_quotas = create_quotas(args.n3, args.lecturerupperquotas)

            instance = self.create_instance(
                args.n1,
                args.n2,
                args.n3,
                pref_lists_students, 
                st_ties,
                project_lecturers,
                lower_quotas,
                upper_quotas,
                pref_lists_lecturers, 
                lec_ties,
                lec_lower_quotas,
                lec_targets,
                lec_upper_quotas,
                instance_info)

            f = open(args.outputdirectory + '/' + str(instance_number) + 
            '.txt', 'w')
            f.write(instance)
            f.close()


    def create_project_lecturers(self, n2, n3):
        """Returns evenly distributed lecturers for projects.

        Args:
            n2: The number of projects.
            n3: The number of lecturers.

        Returns:
            Evenly distributed lecturers for projects.
        """
        num_projects_for_lec_quotient = int(n2 / n3)
        num_projects_for_lec_remainder = int(n2 % n3)

        num_projects_for_each_lecturer = []
        for lec_index in range(n3):
            num_projects_for_each_lecturer.append(num_projects_for_lec_quotient)
            if lec_index < num_projects_for_lec_remainder:
                num_projects_for_each_lecturer[lec_index] += 1

        project_lecturers = []
        for lec_index in range(n3):
            num_to_add = num_projects_for_each_lecturer[lec_index]
            for j in range(num_to_add):
                project_lecturers.append(lec_index + 1)

        return project_lecturers


    def create_student_lec_lists(
        self, pref_lists_students, project_lecturers, n3):
        """Creates lists of which students rank projects of a lecturer.

        Args:
            pref_lists_students: Student preference lists.
            project_lecturers: Which lecturers offer the projects.

        Returns:
            Student lecturer lists.
        """
        student_lists = []
        for st_index in range(len(pref_lists_students)):
            ranked_lecs = [False] * n3
            for proj in pref_lists_students[st_index]:
                lec = project_lecturers[proj - 1]
                ranked_lecs[lec - 1] = True
            student_lec_list = []
            for lec_index, lec_present in enumerate(ranked_lecs):
                if lec_present:
                    student_lec_list.append(lec_index + 1)
            student_lists.append(student_lec_list)
        return student_lists


    def create_instance_info(self, args):
        """Creates a String for instance generation information.

        Args:
            args: User chosen instance parameter information.

        Returns:
            instance_info: Instance gneeration information.
        """
        instance_info = ('instance generation parameters\n'
            'number_of_agents_type_1: ' + str(args.n1) + '\n'
            'number_of_agents_type_2: ' + str(args.n2) + '\n'
            'number_of_agents_type_3: ' + str(args.n3) + '\n'
            'min_pref_list_length: ' + str(args.minpreflistlength) + '\n'
            'max_pref_list_length: ' + str(args.maxpreflistlength) + '\n'
            'ties_probability_1: ' + str(args.ties1) + '\n'
            'ties_probability_2: ' + str(args.ties2) + '\n'
            'sum_agent2_lower_quotas: ' + str(args.lowerquotas) + '\n'
            'sum_agent2_upper_quotas: ' + str(args.upperquotas) + '\n'
            'skew_for_agent_1: ' + str(args.skew) + '\n'
            'sum_agent3_lower_quotas: ' + str(args.lecturerlowerquotas) + '\n'
            'sum_agent3_targets: ' + str(args.lecturertargets) + '\n'
            'sum_agent3_upper_quotas: ' + str(args.lecturerupperquotas) + '\n')

        return instance_info


    def create_instance(
        self,
        n1,
        n2,
        n3,
        pref_lists_students, 
        st_ties,
        project_lecturers,
        lower_quotas,
        upper_quotas,
        pref_lists_lecturers, 
        lec_ties,
        lec_lower_quotas,
        lec_targets,
        lec_upper_quotas,
        instance_info):
        """Outputs an instance to file.

        Args:
            n1: Number of students.
            n2: Number of projects.
            n3: Number of lecturers.
            pref_lists_students: The student preference lists.
            st_ties: Indicating whether a student preference list element is 
              tied with the next.
            lower_quotas: Project lower quotas.
            upper_quotas: Project upper quotas.
            pref_lists_lecturers: The lecturer preference lists.
            lec_ties: Indicating whether a lecturer preference list element is 
              tied with the next.
            lec_lower_quotas: Lecturer lower quotas.
            lec_targets: Lecturer targets.
            lec_upper_quotas: Lecturer upper quotas.
            instance_info: Instance parameter information.
        """
        instance_string = str(n1) + ' ' + str(n2) + ' ' + str(n3) + '\n'

        for x in range(n1):
            student_num = x + 1
            string_pref_list = create_string_pref(
                pref_lists_students[x], st_ties[x])
            prefList = ' '.join(string_pref_list)
            instance_string += (str(student_num) + ": " + prefList + '\n')

        for y in range(n2):
            project_num = y + 1
            instance_string += (str(project_num) + ": " +
                str(lower_quotas[y]) + ": " + str(upper_quotas[y]) + ": " +
                str(project_lecturers[y]) + '\n')

        for z in range(n3):
            lecturer_num = z + 1
            string_pref_list = ''
            if not len(pref_lists_lecturers) == 0:
                string_pref_list = create_string_pref(
                    pref_lists_lecturers[z], lec_ties[z])
            prefList = ' '.join(string_pref_list)
            instance_string += (str(lecturer_num) + ": " + 
                str(lec_lower_quotas[z]) + ": " + str(lec_targets[z]) + ": " + 
                str(lec_upper_quotas[z]) + ": " + prefList + '\n')

        instance_string += '\n' + instance_info

        return instance_string