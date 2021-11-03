"""Solve sudoko"""
from puzzle import puzzle, COL, ROW, CUBE


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
        dirty = set()
        for i in range(9):
            dirty.update([
                (ROW, i),
                (COL, i),
                (CUBE, i)
            ])

        while len(dirty):
            v_type, v_inx = dirty.pop()
            if v_type == ROW:
                vector = self.puzzle.rows[v_inx]
            elif v_type == COL:
                vector = self.puzzle.cols[v_inx]
            else:
                vector = self.puzzle.cubes[v_inx]

            dirty.update(self._rule_single_digit(vector))


    def _rule_single_digit(self, vector):
        digit_count = [[0,-1,-1] for digit in range(10)]
        to_set = set()
        for row, col in vector:
            cell = self.puzzle.board[row][col]
            if type(cell) is int:
                continue
            if len(cell) == 1:
                result, = cell
                to_set.add((row,col, result))
            else:
                for digit in self.puzzle.board[row][col]:
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
            self.puzzle.print_progress(f"ALONE DIGIT {row},{col} -> {digit}")
            dirty.update(self.puzzle.set_cell(row, col, digit))
        return dirty
