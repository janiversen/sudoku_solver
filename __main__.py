"""Presentation and run"""
import sys

from solver import solver

if __name__ != "__main__":
    print("sudoku_solver need to run directly from command line")
    sys.exit(-1)

fixed_cells_simple = [
    (0,5,9), (0,7,4),
    (1,2,4), (1,3,3), (1,5,2), (1,6,6), (1,7,5), (1,8,7),
    (2,4,5), (2,7,1), (2,8,8),
    (3,2,3), (3,3,9), (3,5,8), (3,6,1), (3,8,5),
    (4,2,2), (4,4,4), (4,5,5), (4,7,6),
    (5,0,9), (5,5,6), (5,6,7), (5,8,4),
    (6,2,9), (6,3,5), (6,4,6),
    (7,1,6), (7,4,2), (7,5,3), (7,6,5),
    (8,1,3), (8,3,4)

    # 9536 -> Facil
    # 5 7 8 6 1 9 2 4 3
    # 1 9 4 3 8 2 6 5 7
    # 3 2 6 7 5 4 9 1 8
    # 6 4 3 9 7 8 1 2 5
    # 7 8 2 1 4 5 3 6 9
    # 9 5 1 2 3 6 7 8 4
    # 8 1 9 5 6 7 4 3 2
    # 4 6 7 8 2 3 5 9 1
    # 2 3 5 4 9 1 8 7 6
]

fixed_cells_complex = [
    (0,2,7), (0,7,9),
    (1,4,2), (1,6,1),
    (2,4,5), (2,5,4), (2,6,8),
    (3,1,6), (3,6,7), (3,7,5), (3,8,8),
    (4,0,2), (4,1,8), (4,2,5), (4,4,7), (4,7,3),
    (5,1,3),
    (6,2,4), (6,5,5), (6,6,9),
    (7,0,9), (7,1,7), (7,3,2), (7,7,6),
    (8,0,5), (8,2,3)

    # 39573 -> Muy dificil
    # 1 4 7 6 8 3 5 9 2
    # 8 5 6 9 2 7 1 4 3
    # 3 9 2 1 5 4 8 7 6
    # 4 6 9 3 1 2 7 5 8
    # 2 8 5 4 7 9 6 3 1
    # 7 3 1 5 6 8 4 2 9
    # 6 2 4 8 3 5 9 1 7
    # 9 7 8 2 4 1 3 6 5
    # 5 1 3 7 9 6 2 8 4
]

fixed_cells_extreme = [
    (0,1,2), (0,6,7), (0,7,3),
    (1,4,9), (1,5,7), (1,6,2),
    (2,3,4), (2,8,6),
    (3,0,3), (3,1,9), (3,4,1),
    (4,4,7),
    (5,0,8), (5,3,6), (5,6,1),
    (6,3,9), (6,5,3), (6,8,8),
    (7,1,4), (7,6,3), (7,8,5),
    (8,5,1), (8,7,2)

    # 2271 -> Extreme
]

if len(sys.argv) == 2:
    if sys.argv[1] == "simple":
        fixed_cells = fixed_cells_simple
    elif sys.argv[1] == "complex":
        fixed_cells = fixed_cells_complex
    elif sys.argv[1] == "extreme":
        fixed_cells = fixed_cells_extreme
    else:
        print("Illegal argument")
        sys.exit(-1)
else:
    fixed_cells = fixed_cells_simple

mytest = solver()
mytest.setup(fixed_cells)
mytest.solve()
mytest.print()
if mytest.puzzle.cell_remain != 0:
    print("---- ERROR ----")
    sys.exit(-1)
sys.exit(0)
