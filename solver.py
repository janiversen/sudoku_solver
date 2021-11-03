"""Solve sudoko"""
from puzzle import puzzle, COL, ROW, CUBE, no_solution
from copy import deepcopy

class solution_done(Exception):
    pass


class solver():

    def __init__(self):
        self.puzzle = puzzle()


    def setup(self, fixed_cells):
        for row,col,val in fixed_cells:
            self.puzzle.set_cell(row, col, val)


    def print(self):
        if self.puzzle.cell_remain:
            self.puzzle.print()
        else:
            self.puzzle.print_final()


    def solve(self):
        self.puzzle.in_setup = False
        self.puzzle.print_progress(f"Puzzle with {self.puzzle.cell_remain} unresolved cells")
        dirty = set()
        for i in range(9):
            dirty.update([
                (ROW, i),
                (COL, i),
                (CUBE, i)
            ])
        self._run_solver(self.puzzle, dirty)
        if self.puzzle.cell_remain > 0:
            self.puzzle.print_progress(f"Puzzle contains {self.puzzle.cell_remain} unresolved cells after solver")
            self.puzzle.in_setup = True
            self.depth_max = 0
            try:
                self._run_crunch(deepcopy(self.puzzle), 0, 0, 0, 0)
            except solution_done:
                pass


    def _run_crunch(self, puzzle, depth, s_row, s_col, s_digit):
        depth += 1
        if depth > self.depth_max:
            self.depth_max = depth
            print(f"--> max depth: {depth} vector {len(puzzle.cells)}")
        if s_digit > 0:
            dirty = puzzle.set_cell(s_row, s_col, s_digit)
            self._run_solver(puzzle, dirty)
        if len(puzzle.cells) == 0:
            self.puzzle = puzzle
            raise solution_done()
        row, col = puzzle.cells.pop()
        cell = puzzle.board[row][col]
        for digit in cell:
            try:
                self._run_crunch(deepcopy(puzzle), depth, row, col, digit)
            except no_solution as exc:
                continue

    def _run_solver(self, puzzle, dirty):
        while len(dirty):
            v_type, v_inx = dirty.pop()
            if v_type == ROW:
                vector = puzzle.rows[v_inx]
            elif v_type == COL:
                vector = puzzle.cols[v_inx]
            else:
                vector = puzzle.cubes[v_inx]
                dirty.update(self._rule_cube_vector(puzzle, vector))

            dirty.update(self._rule_single_digit(puzzle, vector))


    def _rule_single_digit(self, puzzle, vector):
        digit_count = [[0,-1,-1] for digit in range(10)]
        to_set = set()
        for row, col in vector:
            cell = puzzle.board[row][col]
            if type(cell) is int:
                continue
            if len(cell) == 1:
                result, = cell
                to_set.add((row,col, result))
            else:
                for digit in puzzle.board[row][col]:
                    digit_count[digit][0] += 1
                    digit_count[digit][1] = row
                    digit_count[digit][2] = col

        for digit in range(1,10):
            if digit_count[digit][0] == 1:
                to_set.add((
                    digit_count[digit][1],
                    digit_count[digit][2],
                    digit
                ))

        dirty = set()
        while len(to_set):
            row, col, digit = to_set.pop()
            puzzle.print_progress(f"ALONE DIGIT {row},{col} -> {digit}")
            dirty.update(puzzle.set_cell(row, col, digit))
        return dirty


    def _rule_cube_vector(self, puzzle, vector):
        digit_check = [[-1,-1, set()] for digit in range(10)]
        to_remove = set()
        for row, col in vector:
            cell = puzzle.board[row][col]
            for digit in cell:
                digit_check[digit][2].add((row, col))
                if digit_check[digit][0] == -1:
                    digit_check[digit][0] = row
                elif digit_check[digit][0] != row:
                    digit_check[digit][0] = -2

                if digit_check[digit][1] == -1:
                    digit_check[digit][1] = col
                elif digit_check[digit][1] != col:
                    digit_check[digit][1] = -2

        dirty = set()
        for digit in range(1,10):
            row = digit_check[digit][0]
            col = digit_check[digit][1]
            loc = digit_check[digit][2]
            if row >= 0:
                puzzle.print_progress(f"DIGIT {digit} only in row {row} of cube remove in row")
                dirty.update(puzzle.remove_val(row, -1, -1, digit, exclude=loc))
            if col >= 0:
                puzzle.print_progress(f"DIGIT {digit} only in col {col} of cube remove in col")
                dirty.update(puzzle.remove_val(-1, col, -1, digit, exclude=loc))
        return dirty
