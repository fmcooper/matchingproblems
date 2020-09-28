import matcher
import sys

"""Simple main class to run the Lp solver over an SPA-STL instance.

SPA-STL is the Student-Project Allocation problem with lecturer preferences over
Students including Ties and Lecturer targets.
"""
if __name__ == "__main__":
    m = matcher.create(sys.argv[1:])
    m.solve(timeLimit=1)
    # print(m.get_debug())
    print(m.get_results_short())
    # print(m.get_results_long())
