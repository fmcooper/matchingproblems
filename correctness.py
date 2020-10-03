import datetime
import os
import sys

"""Script to run correctness tests."""

# Experiments to correctness test of the form A, B, C where
# A = The brute force directory with optimal values
# B = The directory with results to test (note file names must exactly match
# with the corresponding files in the brute force directory)
# C = The optimisation to test.
experiments = [
    ('./Evaluations/hr/bruteforce/', './Evaluations/hr/genmax/', '-genmax'),
    ('./Evaluations/hr/bruteforce/', './Evaluations/hr/gremax/', '-gremax'),
    ('./Evaluations/hr/bruteforce_pc/', './Evaluations/hr/gre_pc/', '-gre'),
    ('./Evaluations/spa/bruteforce/', './Evaluations/spa/genmax/', '-genmax'),
    ('./Evaluations/spa_onesided/bruteforce/', 
        './Evaluations/spa_onesided/genmax/', '-genmax'),
    ('./Evaluations/spa/bruteforce/', './Evaluations/spa/gremax/', '-gremax'),
]

# Stability experiments to correctness test, only of the form
stability_dirs = ['./Evaluations/spa_no_lq/stable/',]


def get_optimal(opt_file, optimisation):
    """Returns the optimal value given the specified optimisation.

    Args:
      opt_file: The file with optimal results.
      optimisation: The optimisation value to return.

    Returns:
      Optimal value.
    """

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
    """Returns the optimal value found using the IP.

    Args:
      res_file: The file with IP results.
      optimisation: The optimisation value to return.

    Returns:
      Optimal value.
    """

    f = open(res_file, "r")
    for line in f:
        if (optimisation == '-genmax' or optimisation == '-gremax' or
            optimisation == '-gre'):
            if 'profile' in line:
                spl = line.split()
                profile = ' '.join(spl[1:])
                return profile


def get_stable(res_file):
    """Returns whether the matching was found to be stable.

    Args:
      res_file: The file with IP results.

    Returns:
      Whether the matching was found to be stable.
    """

    f = open(res_file, "r")
    for line in f:
        if 'stability_correct' in line:
            return line.split()[1]


def run_correctness():
    """Runs correctness tests over all experiments and stability experiments.

    Outputs a correctness report to terminal.
    """

    start_time_string = datetime.datetime.now().strftime("%d %b %Y, %X %Z")
    print('# Correctness results conducted on ' + start_time_string + '\n\n')

    # For each experiment, confirm that the optimal value in the brute force 
    # file matches the value found in the IP result file.
    for experiment in experiments:
        optimal_count = 0
        error_count = 0
        error_files = []
        num_files = len(os.listdir(experiment[0]))
        for i in range(num_files):
            opt_file = experiment[0] + str(i) + '.txt'
            res_file = experiment[1] + str(i) + '.txt'

            if (get_optimal(opt_file, experiment[2]) == 
                get_result(res_file, experiment[2])):
                optimal_count += 1
            else:
                error_count += 1
                error_files.append(res_file)

        # Print experiment results.
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
        # Print error files.
        if not len(error_files) == 0:
            print('files with errors: ' + str(error_files))


    # For each stable directory, confirm that the each file produced a stable
    # matching.
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

        # Print stability results.
        print(
            'stable_dir:', 
            stable_dir, 
            'num_stable:', 
            stable_count, 
            'non_stable_count:', 
            non_stable_count)
        # Print error files.
        if not len(error_files) == 0:
            print('files with errors: ' + str(error_files))

if __name__ == "__main__":
    run_correctness()
