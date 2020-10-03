import argparse
from argparse import RawTextHelpFormatter
from .generator_shared import *
import numpy as np
import os
import random
import sys

"""Generates instances of HA, SM and HR (and their variants).

This program generate instances of the House Allocation problem, the Stable
Marriage problem, the Hospitals/Residents problem, and their variants. 
"""

class Generator_ha_sm_hr:

    def generate_instances(self, args):
        """Generates an instance of HA, SM or HR and writes to file.

        Generates and outputs instance of HRT according to user chosen 
        parameters.

        Args:
            args: User chosen instance parameter information.
        """
        if not os.path.exists(args.outputdirectory):
            os.makedirs(args.outputdirectory)

        for instance_number in range(args.numberinstances):
            pref_lists_res, res_ties = create_pref_lists_original(
                args.n1, 
                args.n2, 
                args.minpreflistlength, 
                args.maxpreflistlength, 
                args.ties1, 
                args.skew)  

            pref_lists_hosp, hosp_ties = [], []
            if args.twopl:
                pref_lists_hosp, hosp_ties = create_pref_lists_from_other_lists(
                    pref_lists_res, args.n2, args.ties2)


            instance_info = self.create_instance_info(args)

            lower_quotas = create_quotas(args.n2, args.lowerquotas)
            upper_quotas = create_quotas(args.n2, args.upperquotas)

            instance = self.create_instance(
                args.n1,
                args.n2,
                pref_lists_res, 
                res_ties,
                pref_lists_hosp, 
                hosp_ties,
                lower_quotas,
                upper_quotas,
                instance_info)

            f = open(args.outputdirectory + '/' + str(instance_number) + 
            '.txt', 'w')
            f.write(instance)
            f.close()


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
            'min_pref_list_length: ' + str(args.minpreflistlength) + '\n'
            'max_pref_list_length: ' + str(args.maxpreflistlength) + '\n'
            'ties_probability_1: ' + str(args.ties1) + '\n'
            'ties_probability_2: ' + str(args.ties2) + '\n'
            'sum_agent2_lower_quotas: ' + str(args.lowerquotas) + '\n'
            'sum_agent2_upper_quotas: ' + str(args.upperquotas) + '\n'
            'skew_for_agent_1: ' + str(args.skew) + '\n')

        return instance_info


    def create_instance(
        self, 
        n1,
        n2, 
        pref_lists_residents, 
        res_ties, 
        pref_lists_hospitals, 
        hosp_ties, 
        lower_quotas,
        upper_quotas,
        instance_info):
        """Creates a string instance.

        Args:
            n1: Number of residents.
            n2: Number of hospitals.
            pref_lists_residents: The residents preference lists.
            res_ties: Indicating whether a resident preference list element is 
              tied with the next.
            pref_lists_hospitals: The hospitals preference lists.
            hosp_ties: Indicating whether a hospital preference list element is 
              tied with the next.
            lower_quotas: Hospital lower quotas.
            upper_quotas: Hospital upper quotas.
            instance_info: Instance parameter information.
        """
        instance_string = str(n1) + ' ' + str(n2) + '\n'

        for x in range(n1):
            resident_num = x + 1
            string_pref_list = create_string_pref(
                pref_lists_residents[x], res_ties[x])
            prefList = ' '.join(string_pref_list)
            instance_string += (str(resident_num) + ": " + prefList + '\n')

        for x in range(n2):
            hospital_num = x + 1
            if not len(pref_lists_hospitals) == 0:
                string_pref_list = create_string_pref(
                pref_lists_hospitals[x], hosp_ties[x])
            prefList = ' '.join(string_pref_list)
            instance_string += (str(hospital_num) + ": " + 
                str(lower_quotas[x]) + ": " + str(upper_quotas[x]) + ": " + 
                prefList + '\n')

        instance_string += '\n' + instance_info

        return instance_string
