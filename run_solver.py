from matchingproblems import solver
import sys

"""Simple main class to run the Lp solver over an SPA-STL instance.

SPA-STL is the Student-Project Allocation problem with lecturer preferences over
Students including Ties and Lecturer targets.
"""
if __name__ == "__main__":
    solver = solver.Solver(sys.argv[1:])
    solver.solve()
    print(solver.get_results())


