import os
import sys
import datetime

experiments = [
    ('./Evaluations/hr/bruteforce/', './Evaluations/hr/genmax/', '-genmax'),
    ('./Evaluations/hr/bruteforce/', './Evaluations/hr/gremax/', '-gremax'),
    ('./Evaluations/hr/bruteforce_pc/', './Evaluations/hr/gre_pc/', '-gre'),
    ('./Evaluations/spa/bruteforce/', './Evaluations/spa/genmax/', '-genmax'),
    ('./Evaluations/spa_onesided/bruteforce/', './Evaluations/spa_onesided/genmax/', '-genmax'),
    ('./Evaluations/spa/bruteforce/', './Evaluations/spa/gremax/', '-gremax'),
]

stability_dirs = ['./Evaluations/spa_no_lq/stable/',]


def get_optimal(opt_file, optimisation):
    f = open(opt_file, "r")
    profile = ''
    for line in f:
        if optimisation == '-genmax' and 'optimal_generousmaxprofile' in line:
            spl = line.split()
            profile = ' '.join(spl[1:])
            return profile
        if optimisation == '-gremax' and 'optimal_greedymaxprofile' in line:
            spl = line.split()
            profile = ' '.join(spl[1:])
            return profile
        if optimisation == '-gre' and 'optimal_greedyprofile' in line:
            spl = line.split()
            profile = ' '.join(spl[1:])
            return profile


def get_result(res_file, optimisation):
    f = open(res_file, "r")
    for line in f:
        if (optimisation == '-genmax' or optimisation == '-gremax' or
            optimisation == '-gre'):
            if 'profile' in line:
                spl = line.split()
                profile = ' '.join(spl[1:])
                return profile


def get_stable(res_file):
    f = open(res_file, "r")
    for line in f:
        if 'stability_correct' in line:
            return line.split()[1]


if __name__ == "__main__":

    start_time_string = datetime.datetime.now().strftime("%d %b %Y, %X %Z")
    print('# Correctness results conducted on ' + start_time_string + '\n\n')

    for experiment in experiments:
        optimal_count = 0
        error_count = 0
        error_files = []
        num_files = len(os.listdir(experiment[0]))
        for i in range(num_files):
            opt_file = experiment[0] + str(i) + '.txt'
            res_file = experiment[1] + str(i) + '.txt'

            if get_optimal(opt_file, experiment[2]) == get_result(res_file, experiment[2]):
                optimal_count += 1
            else:
                print(res_file, get_optimal(opt_file, experiment[2]), get_result(res_file, experiment[2]))
                error_count += 1
                error_files.append(res_file)

        print(
            'optimal_dir:', 
            experiment[0], 
            'result_dir:', 
            experiment[1], 
            'optimisation:',
            experiment[2], 
            'num_optimal:', 
            optimal_count, 
            'num_error:', 
            error_count)
        
        if not len(error_files) == 0:
            print('files with errors: ' + error_files)

    for stable_dir in stability_dirs:
        stable_count = 0
        non_stable_count = 0
        error_files = []
        num_files = len(os.listdir(stable_dir))
        for i in range(num_files):
            file = stable_dir + str(i) + '.txt'
            if get_stable(file) == 'True':
                stable_count += 1
            else:
                non_stable_count += 1
                error_files.append(res_file)

        print(
            'stable_dir:', 
            stable_dir, 
            'num_stable:', 
            stable_count, 
            'non_stable_count:', 
            non_stable_count)

        if not len(error_files) == 0:
            print('files with errors: ' + str(error_files))
