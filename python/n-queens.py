"""
  OR-tools solution to the N-queens problem.
"""

from __future__ import print_function
import sys
from ortools.constraint_solver import pywrapcp
import numpy as np

def main(N):
  # Creates the solver.
  solver = pywrapcp.Solver("n-queens")
  # Creates the variables.
  # The array index is the column, and the value is the row.
  queens = [solver.IntVar(0, N - 1, "x%i" % i) for i in range(N)]
  # Creates the constraints.

  # All rows must be different.
  solver.Add(solver.AllDifferent(queens))
  
  # trim the solution by setting the first location
  # TODO: getting rid of all symmetry would be better, this will do for now
  solver.Add(queens[0] == 0)

  # All columns must be different because the indices of queens are all different.

  # No two queens can be on the same diagonal.
  #solver.Add(solver.AllDifferent([queens[i] + i for i in range(N)]))
  #solver.Add(solver.AllDifferent([queens[i] - i for i in range(N)]))

  db = solver.Phase(queens,
                    solver.CHOOSE_FIRST_UNBOUND,
                    solver.ASSIGN_RANDOM_VALUE)
  solver.NewSearch(db)

  # Iterates through the solutions, displaying each.
  solutions = []
  while solver.NextSolution():
    points = []
    for i in range(N):
      points.append((i, queens[i].Value()))
    # TODO: center the points for the calculation
    pointsStd = np.std(map(np.linalg.norm, points))
    solutions.append((points, pointsStd))

  solver.EndSearch()

  print()
  print("Solutions found:", len(solutions))
  print("Time:", solver.WallTime(), "ms")

  arranged = [str(s[0]) + "\n" for s in sorted(solutions, key=lambda sol: sol[1])]
  with open(str(N) + ".points", "wb") as fp:
    fp.writelines(arranged)
      

# By default, solve the 8x8 problem.
N = 7

if __name__ == "__main__":
  if len(sys.argv) > 1:
    N = int(sys.argv[1])
  main(N)