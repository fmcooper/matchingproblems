
from .model import Model
from .model import Pair
from .enums import Instance_options

def _get_simple_pref_list_and_ranks(pref_list):
    simp_pref_list = []
    simp_ranks = []
    rank = 1
    in_tie = False

    for i in range(len(pref_list)):
        if '(' in pref_list[i]:
            elem_num = int(pref_list[i].replace('(', ''))
            simp_pref_list.append(elem_num)
            simp_ranks.append(rank)
            in_tie = True

        elif ')' in pref_list[i]:
            elem_num = int(pref_list[i].replace(')', ''))
            simp_pref_list.append(elem_num)
            simp_ranks.append(rank)
            rank+=1
            in_tie = False

        else:
            simp_pref_list.append(int(pref_list[i]))
            simp_ranks.append(rank)
            if not in_tie:
                rank+=1

    return simp_pref_list, simp_ranks


def _create_pairs_row(model, st_prefs, st_num):
    pairs_row = []
    simp_st_prefs, simp_st_ranks = _get_simple_pref_list_and_ranks(st_prefs)

    for i in range(len(simp_st_prefs)):
            pairs_row.append(Pair(st_num, simp_st_prefs[i], simp_st_ranks[i]))
            in_tie = True

    return pairs_row


def _create_student_ranks(model, lec_prefs, lec_num):
    student_ranks = {}
    simp_lec_prefs, simp_lec_ranks = _get_simple_pref_list_and_ranks(lec_prefs)

    for i, _ in enumerate(simp_lec_prefs):
        student_ranks[(lec_num, simp_lec_prefs[i])] = simp_lec_ranks[i]

    return student_ranks


def _set_lecturers(model, project_lecturers):
    for st_pairs in model.pairs:
        for st_pr_pair in st_pairs:
            st_pr_pair.set_lecturer(project_lecturers[st_pr_pair.project_index])
        

def _set_lecturer_ranks(model, lec_st_ranks):
    for st_pairs in model.pairs:
        for st_pr_pair in st_pairs:
            rank = lec_st_ranks[(st_pr_pair.lecturerID, st_pr_pair.studentID)]
            st_pr_pair.set_lecturer_rank(rank)
        






def _import_from_file(filename, instance_options):
    model = Model()
    project_lecturers = []
    lecturer_student_ranks = {}

    with open(filename) as f:
        for index, line in enumerate(f):
            line_split = line.replace(':', '').split()

            #first line
            if index == 0:
                first_line = line.split()
                model.num_students = int(first_line[0])
                model.num_projects = int(first_line[1])
                if instance_options[Instance_options.NUMAGENTS] == 2:
                    model.num_lecturers = int(first_line[1])
                if instance_options[Instance_options.NUMAGENTS] == 3:
                    model.num_lecturers = int(first_line[2])

            # student preference lists
            elif index < model.num_students + 1:
                st_prefs = line_split[1:]
                st_num = index
                pairs_row = _create_pairs_row(model, st_prefs, st_num)
                model.pairs.append(pairs_row)

            # projects
            elif index < model.num_students + model.num_projects + 1:
                # SPA
                if instance_options[Instance_options.NUMAGENTS] == 3:
                    model.proj_lower_quotas.append(int(line_split[1]))
                    model.proj_upper_quotas.append(int(line_split[2]))
                    project_lecturers.append(int(line_split[3]))

                # HR
                if instance_options[Instance_options.NUMAGENTS] == 2:
                    model.proj_lower_quotas.append(int(line_split[1]))
                    model.proj_upper_quotas.append(int(line_split[2]))
                    proj_num = index - (model.num_students)
                    project_lecturers.append(proj_num)
                    model.lec_lower_quotas.append(int(line_split[1]))
                    model.lec_targets.append(int(line_split[2]))
                    model.lec_upper_quotas.append(int(line_split[2]))
                    proj_num = len(model.proj_lower_quotas)

                    # if hospital preference lists are present, add them to the model
                    if instance_options[Instance_options.TWOPL]:
                        additional_hosp_ranks = _create_student_ranks(model, line_split[3:], proj_num)
                        lecturer_student_ranks.update(additional_hosp_ranks)


            # SPA only - lecturer preference lists
            elif index < model.num_students + model.num_projects + model.num_lecturers + 1 and instance_options[Instance_options.NUMAGENTS] == 3:
                model.lec_lower_quotas.append(int(line_split[1]))
                model.lec_targets.append(int(line_split[2]))
                model.lec_upper_quotas.append(int(line_split[3]))
                rank = 1
                lec_num = index - (model.num_students + model.num_projects)

                # if lecturer preference lists are present, add them to the model
                if instance_options[Instance_options.TWOPL]:
                    additional_lec_st_ranks = _create_student_ranks(model, line_split[4:], lec_num)
                    lecturer_student_ranks.update(additional_lec_st_ranks)

    model.proj_lecturers = project_lecturers
    _set_lecturers(model, project_lecturers)
    if instance_options[Instance_options.TWOPL]:
        _set_lecturer_ranks(model, lecturer_student_ranks)

    

    return model




def import_model(filename, instance_options):
    model = _import_from_file(filename, instance_options)
    model.set_project_lists()
    model.set_lecturer_lists()
    model.set_rank_lists()
    return model
    
    







