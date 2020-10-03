#!/bin/bash

# Variables.
PREPATH="./Evaluations/"			# Location of your results.
PARALLEL_OPTS="--jobs 3 --bar"		# Changes the number of parallel jobs running.


# Function to run the solver.
runSolver() {
	INSTANCE=$1
	RESNAME=$2
	SOLVER_OPTIONS=${@:3}
	DIR=$(dirname $INSTANCE)
	RESDIR=$(sed "s/instances/$RESNAME/g" <<< $DIR)
	RESFILE=$(sed "s/instances/$RESNAME/g" <<< $INSTANCE)
	mkdir -p $RESDIR
	python run_solver.py -f $INSTANCE $SOLVER_OPTIONS > $RESFILE
	echo "solver completed" >> $RESFILE 
}

export -f runSolver

NUMINSTANCES=5

# HR instances.
INSTANCES_DIR_HR="${PREPATH}hr/instances"
GENERATOR_OPTIONS_HR="-numinst $NUMINSTANCES -o $INSTANCES_DIR_HR -mp hr -n1 6 -n2 4 -pmin 2 -pmax 4 -t1 0.2 -t2 0.2 -skew 5 -lq 4 -uq 6 -twopl"
python run_generator.py $GENERATOR_OPTIONS_HR

# HR solving generous maximum.
ls -d "$INSTANCES_DIR_HR"/* | parallel $PARALLEL_OPTS runSolver {} genmax -na 2 -maxsize 1 -gen 2 -twopl
# HR solving greedy maximum.
ls -d "$INSTANCES_DIR_HR"/* | parallel $PARALLEL_OPTS runSolver {} bruteforce -na 2 -twopl -bf
# HR solving brute force for correctness.
ls -d "$INSTANCES_DIR_HR"/* | parallel $PARALLEL_OPTS runSolver {} gremax -na 2 -maxsize 1 -gre 2 -twopl
# HR solving greedy with project closures.
ls -d "$INSTANCES_DIR_HR"/* | parallel $PARALLEL_OPTS runSolver {} gre_pc -na 2 -gre 1 -twopl -pc
# HR solving brute force with project closures for correctness.
ls -d "$INSTANCES_DIR_HR"/* | parallel $PARALLEL_OPTS runSolver {} bruteforce_pc -na 2 -twopl -bf -pc


# SPA one-sided preference list instances.
INSTANCES_DIR_SPA_ONESIDED="${PREPATH}spa_onesided/instances"
GENERATOR_OPTIONS_SPA_ONESIDED="-numinst $NUMINSTANCES -o $INSTANCES_DIR_SPA_ONESIDED -mp spa -n1 6 -n2 8 -n3 4 -pmin 3 -pmax 5 -t1 0.2 -t2 0.2 -skew 5 -lq 4 -uq 10 -llq 1 -lt 4 -luq 10"
python run_generator.py $GENERATOR_OPTIONS_SPA_ONESIDED

# SPA one-sided solving generous maximum.
ls -d "$INSTANCES_DIR_SPA_ONESIDED"/* | parallel $PARALLEL_OPTS runSolver {} genmax -na 3 -maxsize 1 -gen 2
# SPA one-sided solving brute force for correctness.
ls -d "$INSTANCES_DIR_SPA_ONESIDED"/* | parallel $PARALLEL_OPTS runSolver {} bruteforce -na 3 -bf


# SPA instances.
INSTANCES_DIR_SPA="${PREPATH}spa/instances"
GENERATOR_OPTIONS_SPA="-numinst $NUMINSTANCES -o $INSTANCES_DIR_SPA -mp spa -n1 6 -n2 8 -n3 4 -pmin 3 -pmax 5 -t1 0.2 -t2 0.2 -skew 5 -lq 4 -uq 10 -llq 1 -lt 4 -luq 10 -twopl"
python run_generator.py $GENERATOR_OPTIONS_SPA

# SPA solving generous maximum.
ls -d "$INSTANCES_DIR_SPA"/* | parallel $PARALLEL_OPTS runSolver {} genmax -na 3 -maxsize 1 -gen 2 -twopl
# SPA solving greedy maximum.
ls -d "$INSTANCES_DIR_SPA"/* | parallel $PARALLEL_OPTS runSolver {} gremax -na 3 -maxsize 1 -gre 2 -twopl
# SPA solving brute force for correctness.
ls -d "$INSTANCES_DIR_SPA"/* | parallel $PARALLEL_OPTS runSolver {} bruteforce -na 3 -twopl -bf


# SPA no lower quotas instances.
INSTANCES_DIR_SPA_NO_LQ="${PREPATH}spa_no_lq/instances"
GENERATOR_OPTIONS_SPA_NO_LQ="-numinst $NUMINSTANCES -o $INSTANCES_DIR_SPA_NO_LQ -mp spa -n1 6 -n2 8 -n3 4 -pmin 3 -pmax 5 -t1 0.2 -t2 0.2 -skew 5 -lq 0 -uq 10 -llq 0 -lt 4 -luq 10 -twopl"
python run_generator.py $GENERATOR_OPTIONS_SPA_NO_LQ

# SPA no lower quotas solving stable.
ls -d "$INSTANCES_DIR_SPA_NO_LQ"/* | parallel $PARALLEL_OPTS runSolver {} stable -na 3 -stab -twopl


# Generate correctness testing report according to the files specified in correctness.py.
> correctness_report.txt
python correctness.py >> correctness_report.txt

echo "all processes complete"
