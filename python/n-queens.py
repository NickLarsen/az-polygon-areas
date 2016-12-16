"""
  OR-tools solution to the N-queens problem.
"""

from __future__ import print_function
import sys
from ortools.constraint_solver import pywrapcp
import numpy as np
import symmetry as sym

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
  # solver.Add(queens[0] == 3)

  # All columns must be different because the indices of queens are all different.

  # No two queens can be on the same diagonal.
  #solver.Add(solver.AllDifferent([queens[i] + i for i in range(N)]))
  #solver.Add(solver.AllDifferent([queens[i] - i for i in range(N)]))

  db = solver.Phase(queens, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_RANDOM_VALUE)
  solver.NewSearch(db)

  # Iterates through the solutions, displaying each.
  seen = set()
  feasy = open(str(N) + ".points", "w+")
  fcsv = open(str(N) + "-points.csv", "w+")
  while solver.NextSolution():
    points = []
    for i in range(N):
      points.append((i+1, queens[i].Value()+1))
  
    pointsCanonical = sym.canonicalHash([queens[i].Value() for i in range(N)])
    if pointsCanonical in seen: continue
    seen.add(pointsCanonical)

    solutionNumber = len(seen)
    output = [str(p[0]) + "," + str(p[1]) + "," + str(solutionNumber) + "\n" for p in points]
    fcsv.writelines(output)
    output = str(points) + "\n"
    feasy.write(output)

    if solutionNumber >= 1000000: break

  solver.EndSearch()

  print()
  print("Solutions found:", len(seen))
  print("Time:", solver.WallTime(), "ms")

# By default, solve the 8x8 problem.
N = 7

if __name__ == "__main__":
  if len(sys.argv) > 1:
    N = int(sys.argv[1])
  main(N)