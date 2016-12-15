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
  halfN = N / 2.0
  with open(str(N) + ".points", "w+") as fp:
    while solver.NextSolution():
      points = []
      centers = []
      for i in range(N):
        points.append((i+1, queens[i].Value()+1))
        centers.append((i-halfN,queens[i].Value()-halfN))
    
      pointsCanonical = sym.canonicalHash([queens[i].Value() for i in range(N)])
      if pointsCanonical in seen: continue
      seen.add(pointsCanonical)

      pointsStd = np.std(map(np.linalg.norm, centers))
      outputline = str(points) + " " + str(pointsStd) + "\n"
      fp.write(outputline)

    solver.EndSearch()

  print()
  print("Solutions found:", len(solutions))
  print("Time:", solver.WallTime(), "ms")

  arranged = [str(s[0]) + " " + str(s[1]) + "\n" for s in sorted(solutions, key=lambda sol: sol[1])]
  with open(str(N) + ".points", "w+") as fp:
    fp.writelines(arranged)   

# By default, solve the 8x8 problem.
N = 7

if __name__ == "__main__":
  if len(sys.argv) > 1:
    N = int(sys.argv[1])
  main(N)