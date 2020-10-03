#!/bin/bash

# variables
PREPATH="./Evaluations/"			# location of your results


python run_solver.py -f ${PREPATH}spa_no_lq/instances/0.txt -na 3 -gre 1 -twopl


echo "single run complete"