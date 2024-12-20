from matchingproblems import solver
import sys

if __name__ == "__main__":
    solver = solver.Solver(sys.argv[1:])
    solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    # print(solver.get_debug())
    # print(solver.get_results_long())
    # print(solver.get_results_short())
    print(solver.get_results())