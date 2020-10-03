#!/bin/bash

# variables
PREPATH="./Evaluations/"			# location of your results
PARALLEL_OPTS="--jobs 3 --bar"		# changes the number of parallel jobs running


# generate instances
INSTANCES_DIR_HR="./Evaluations/hr/instances"
INSTANCES_DIR_SPA_ONESIDED="./Evaluations/spa_onesided/instances"
INSTANCES_DIR_SPA="./Evaluations/spa/instances"
INSTANCES_DIR_SPA_NO_LQ="./Evaluations/spa_no_lq/instances"
GENERATOR_OPTIONS_HR="-numinst 100 -o $INSTANCES_DIR_HR -mp hr -n1 6 -n2 4 -pmin 2 -pmax 4 -t1 0.2 -t2 0.2 -skew 5 -lq 4 -uq 6 -twopl"
GENERATOR_OPTIONS_SPA_ONESIDED="-numinst 100 -o $INSTANCES_DIR_SPA_ONESIDED -mp spa -n1 6 -n2 8 -n3 4 -pmin 3 -pmax 5 -t1 0.2 -t2 0.2 -skew 5 -lq 4 -uq 10 -llq 1 -lt 4 -luq 10"
GENERATOR_OPTIONS_SPA="-numinst 100 -o $INSTANCES_DIR_SPA -mp spa -n1 6 -n2 8 -n3 4 -pmin 3 -pmax 5 -t1 0.2 -t2 0.2 -skew 5 -lq 4 -uq 10 -llq 1 -lt 4 -luq 10 -twopl"
GENERATOR_OPTIONS_SPA_NO_LQ="-numinst 100 -o $INSTANCES_DIR_SPA_NO_LQ -mp spa -n1 6 -n2 8 -n3 4 -pmin 3 -pmax 5 -t1 0.2 -t2 0.2 -skew 5 -lq 0 -uq 10 -llq 0 -lt 4 -luq 10 -twopl"
python run_generator.py $GENERATOR_OPTIONS_HR
python run_generator.py $GENERATOR_OPTIONS_SPA_ONESIDED
python run_generator.py $GENERATOR_OPTIONS_SPA
python run_generator.py $GENERATOR_OPTIONS_SPA_NO_LQ


# do the experiments
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

# HR standard
LP_SOLVER_OPTIONS_HR_GENMAX="-na 2 -maxsize 1 -gen 2 -twopl"
LP_SOLVER_OPTIONS_HR_GREMAX="-na 2 -maxsize 1 -gre 2 -twopl"
BF_SOLVER_OPTIONS="-na 2 -twopl -bf"
ls -d "$INSTANCES_DIR_HR"/* | parallel $PARALLEL_OPTS runSolver {} genmax $LP_SOLVER_OPTIONS_HR_GENMAX
ls -d "$INSTANCES_DIR_HR"/* | parallel $PARALLEL_OPTS runSolver {} gremax $LP_SOLVER_OPTIONS_HR_GREMAX
ls -d "$INSTANCES_DIR_HR"/* | parallel $PARALLEL_OPTS runSolver {} bruteforce $BF_SOLVER_OPTIONS

# HR project closures
LP_SOLVER_OPTIONS_HR_GRE_PC="-na 2 -gre 1 -twopl -pc"
BF_SOLVER_OPTIONS_PC="-na 2 -twopl -bf -pc"
ls -d "$INSTANCES_DIR_HR"/* | parallel $PARALLEL_OPTS runSolver {} gre_pc $LP_SOLVER_OPTIONS_HR_GRE_PC
ls -d "$INSTANCES_DIR_HR"/* | parallel $PARALLEL_OPTS runSolver {} bruteforce_pc $BF_SOLVER_OPTIONS_PC

# SPA one sided
LP_SOLVER_OPTIONS_SPA_GENMAX="-na 3 -maxsize 1 -gen 2"
BF_SOLVER_OPTIONS_ONESIDED="-na 3 -bf"
ls -d "$INSTANCES_DIR_SPA_ONESIDED"/* | parallel $PARALLEL_OPTS runSolver {} genmax $LP_SOLVER_OPTIONS_SPA_GENMAX
ls -d "$INSTANCES_DIR_SPA_ONESIDED"/* | parallel $PARALLEL_OPTS runSolver {} bruteforce $BF_SOLVER_OPTIONS_ONESIDED

# SPA standard
LP_SOLVER_OPTIONS_SPA_GENMAX="-na 3 -maxsize 1 -gen 2 -twopl"
LP_SOLVER_OPTIONS_SPA_GREMAX="-na 3 -maxsize 1 -gre 2 -twopl"
BF_SOLVER_OPTIONS="-na 3 -twopl -bf"
ls -d "$INSTANCES_DIR_SPA"/* | parallel $PARALLEL_OPTS runSolver {} genmax $LP_SOLVER_OPTIONS_SPA_GENMAX
ls -d "$INSTANCES_DIR_SPA"/* | parallel $PARALLEL_OPTS runSolver {} gremax $LP_SOLVER_OPTIONS_SPA_GREMAX
ls -d "$INSTANCES_DIR_SPA"/* | parallel $PARALLEL_OPTS runSolver {} bruteforce $BF_SOLVER_OPTIONS

# SPA stable
LP_SOLVER_OPTIONS_SPA_NO_LQ_STABLE="-na 3 -stab -twopl"
ls -d "$INSTANCES_DIR_SPA_NO_LQ"/* | parallel $PARALLEL_OPTS runSolver {} stable $LP_SOLVER_OPTIONS_SPA_NO_LQ_STABLE

# stats
> correctness_report.txt
python correctness.py >> correctness_report.txt
# python stats/pythonStats.py $PREPATH


echo "all processes complete"