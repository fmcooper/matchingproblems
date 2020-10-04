# matchingproblems

This python package can generate and solve single or multiple matching problem instances using the PuLP Linear Program (LP) Solver.

It can be used both for individual real-world runs (for example to assign students to projects at your university), and for experimental work including correctness testing of the LP using a brute force approach (smaller instances only).

1) Installation
2) Generator
3) Solver
4) Testing details

## 1) Installation

The simplest way to install this package is via Pip.

```
pip install matchingproblems
```

Alternatively the package may be downloaded from this [git repository](https://github.com/fmcooper/matchingproblems) and installed manually.

## 2) Generator
Instances of the following types can be generated:
* HA - House Allocation Problem (and variants)
* SM - Stable Marriage Problem (and variants)
* HR - Hospital/Residents Problem (and variants)
* SPA - Student-Project Allocation Problem (and variants)

For a definition of each of these problems, please see Chapter 2 of [this thesis](http://theses.gla.ac.uk/81622/).

Example run_generator.py script to run the generator:

```
from matchingproblems import generator
import sys

if __name__ == "__main__":
    generator = generator.Generator(sys.argv[1:])
```

This program may then be called as follows:

```
python run_generator.py [-h] -numinst NUMBERINSTANCES -o OUTPUTDIRECTORY -mp {ha,sm,hr,spa} 
                        [-twopl] [-skew SKEW] [-n1 N1] [-n2 N2] [-n3 N3] 
                        [-pmin MINPREFLISTLENGTH] [-pmax MAXPREFLISTLENGTH] [-t1 TIES1] [-t2 TIES2]
                        [-lq LOWERQUOTAS] [-uq UPPERQUOTAS] [-llq LECTURERLOWERQUOTAS] [-luq LECTURERUPPERQUOTAS] [-lt LECTURERTARGETS]
```

Alternatively, arguments may be defined in the python script itself.

Arguments have the following meanings:

Argument | Meaning
--- | ---
`-h, --help` | Show help message and exit.
`-numinst x, --numberinstances x` | Total number of instances to generate.
`-o x, --outputdirectory x` | Output directory path.
`-mp {ha,sm,hr,spa}, --matchingproblem {ha,sm,hr,spa}` | Matching problem type, as specified above.
`-twopl, --preferencelists2` | Preference lists on both sides of the matching problem.
`-skew x, --linearskew x` | Linear skew for preference lists, a value of x indicates that the most popular agent is x times more popular than the least.
`-n1 x, --numberofagents1 x` | Number of applicants (HA) / men (SM) / residents (HR) / students (SPA).
`-n2 x, --numberofagents2 x` | Number of houses (HA) / hospitals (HR) / projects (SPA).
`-n3 x, --numberofagents3 x` | Number of lecturers (SPA).
`-pmin x, --minpreflistlength x` | Minimum size of preference lists for applicants (HA) / men (SM) / residents (HR) / students (SPA).
`-pmax x, --maxpreflistlength x` | Maximum size of preference lists for applicants (HA) / men (SM) / residents (HR) / students (SPA).
`-t1 x, --ties1 x` | Probability of ties for applicants (HA) / men (SM) / residents (HR) / students (SPA) [0.0, 1.0].
`-t2 x, --ties2 x` | Probability of ties for women (SM) / hospitals (HR) / lecturers (SPA) [0.0, 1.0].
`-lq x, --lowerquotas x` | Sum of lower quotas for houses (HA) / hospitals (HR) / projects (SPA).
`-uq x, --upperquotas x` | Sum of upper quotas for houses (HA) / hospitals (HR) / projects (SPA).
`-llq x, --lecturerlowerquotas x` | Sum of lower quotas for lecturers (SPA).
`-lt x, --lecturertargets x` | Sum of targets for lecturers (SPA).
`-luq x, --lecturerupperquotas x` | Sum of upper quotas for lecturers (SPA).

HA instances require the following arguments to be specified: `-n1 -n2 -pmin -pmax -uq`

SM instances require the following arguments to be specified: `-n1 -pmin -pmax -twopl`

HR instances require the following arguments to be specified: `-n1 -n2 -pmin -pmax -uq -twopl`

SPA instances require the following arguments to be specified: `-n1 -n2 -n3 -pmin -pmax -uq -luq`


    
Two examples of calls to run_generator.py are as follows:
```
# Generates 5 HR instances
python run_generator.py -numinst 5 -o ./hr/instances -mp hr -n1 6 -n2 4 -pmin 2 -pmax 4 -t1 0.2 -t2 0.2 -skew 5 -lq 4 -uq 6 -twopl
```
```
# Generates 5 SPA instances with one-sided preference lists
python run_generator.py -numinst $NUMINSTANCES -o ./spa/instances -mp spa -n1 6 -n2 8 -n3 4 -pmin 3 -pmax 5 -t1 0.2 -t2 0.2 -skew 5 -lq 4 -uq 10 -llq 1 -lt 4 -luq 10 -twopl
```
   
## 3) Solver

Each input instance of HA, SM, HR or SPA is converted into an instance of SPA-STL (the Student-Project Allocation Problem with lecturer preferences over Students including Ties and Lecturer targets) and solved using the PuLP LP Solver.

Example run_solver.py script to run the solver:

```
from matchingproblems import solver
import sys

if __name__ == "__main__":
    solver = solver.Solver(sys.argv[1:])
    solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    # print(solver.get_debug())
    # print(solver.get_results())
    # print(solver.get_results_short())
    print(solver.get_results_long())
```


This program may then be called as follows:

```
python run_solver.py [-h] -f FILENAME -na NUMAGENTS 
                     [-twopl] [-pc] [-stab] [-maxsize MAXSIZE] [-minsize MINSIZE] [-gen GEN]
                     [-gre GRE] [-mincost MINCOST] [-minsqcost MINSQCOST] [-lmb LMB] [-lsb LSB] [-bf]
```

As with the generator, an alternative is to specify arguments in the python script.

Arguments have the following meanings:

Argument | Meaning
--- | ---
`-h, --help` | Show help message and exit.
`-f x, -filename x` | Input file name.
`-na x, -numagents x` | Number of agents in the instance (2 for HA, SM and HR, 3 for SPA).
`-twopl, -twosidedpreferencelists` | Men (SM), Hospital (HR) or lecturer (SPA) preference lists present.
`-pc, -projectclosures` | Project closures allowed.
`-stab, -stability` | Add stability constraints
`-maxsize x, -maximisesize x` | Maximise size at the given optimisation position.
`-minsize x, -minimisesize x` | Minimise size at the given optimisation position.
`-gen x, -generous x` | Performs generous optimisation at the given optimisation position.
`-gre x, -greedy x` | Performs greedy optimisation at the given optimisation position.
`-mincost x, -minimisecost x` | Minimise cost at the given optimisation position.
`-minsqcost x, -minimisesquaredcost x` | Minimises sum of squares of costs at the given optimisation position.
`-lmb x, -loadmaxbalanced x` | Minimises the maximum absolute difference between lecturer occupancy and target at the given optimisation position.
`-lsb x, -loadsumbalanced x` | Minimises the sum of absolute differences between lecturer occupancies and targets at the given optimisation position.
`-bf, -bruteforce` | Solve using the brute force method.


Two examples of calls to run_solver.py are as follows:
```
# Find a generous maximum matching in an HA, SM or HR instance.
python run_solver.py -f ./path/to/instance.txt genmax -na 2 -maxsize 1 -gen 2 -twopl
```
```
# Find optimal assignments for an SPA instance with one sided preference lists using a brute force approach.
python run_solver.py -f ./path/to/instance.txt -na 3 -bf
```       


## 4) Testing details

Unit tests may be run by executing the `test.sh` script in this [git repository](https://github.com/fmcooper/matchingproblems).

Correctness testing which compared output from the LP Solver and brute force programs was conducted on some optimisations. Results for this testing can be seen at this [zenodo repository](10.5281/zenodo.4065148).
