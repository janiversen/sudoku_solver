"""Puzzle data"""
ROW = "row"
COL = "col"
CUBE = "cube"

class puzzle:
    def __init__(self):
        self.board = [[set([cell for cell in range(1,10)])
            for col in range(9)] for row in range(9)]

        self.rows = [set([(row,col) for col in range(9)]) for row in range(9)]
        self.cols = [set([(row,col) for row in range(9)]) for col in range(9)]
        self.cubes = [set([(i1+i2,j1+j2) for i1 in range(3) for j1 in range(3)])
            for i2 in [0,3,6] for j2 in [0,3,6]]
        self.cell_remain = 81
        self.in_setup = True


    def print(self):
        for row in range(9):
            print('-' * (9*8 +1))
            for offset in [1,4,7]:
                for col in range(9):
                    if type(self.board[row][col]) is int:
                        if offset == 4:
                            msg = f"  {self.board[row][col]}   "
                        else:
                            msg = "      "
                    else:
                        msg = ""
                        for i in range(offset, offset+3):
                            if i in self.board[row][col]:
                                msg += f"{i} "
                            else:
                                msg += "  "
                    print(f"| {msg}", end='')
                print('|')
        print('-' * (9*8 +1))
        print(f"--- remaining {self.cell_remain}")


    def print_final(self):
        print('-' * (9*2 +3))
        for row in range(9):
            print('| ', end='')
            for col in range(9):
                print(f"{self.board[row][col]} ", end='')
            print('|')
        print('-' * (9*2 +3))


    def print_progress(self, msg):
        if not self.in_setup:
            print(msg)


    def set_cell(self, row, col, val):
        if type(self.board[row][col]) is int:
            return set()
        self.print_progress(f"-> set cell {row},{col} = {val}")
        self.cell_remain -= 1
        self.board[row][col] = val
        self.rows[row].remove((row,col))
        self.cols[col].remove((row,col))
        cube = int(col/3) + 3* int(row/3)
        self.cubes[cube].remove((row,col))

        dirty = set([
            (ROW, row),
            (COL, col),
            (CUBE, cube)
        ])
        dirty.update(self.remove_val(row, col, cube, val))
        return dirty


    def remove_val(self, row, col, cube, val):
        new_set = []
        vector = set.union(self.rows[row], self.cols[col], self.cubes[cube])
        dirty = set()
        for t_row, t_col in vector:
            cell = self.board[t_row][t_col]
            if type(cell) is int:
                continue
            if val in cell:
                cell.remove(val)
                lx = len(cell)
                if lx == 0:
                    raise Exception("Cell conflict")
                elif lx == 1:
                    result, = cell
                    new_set.append((t_row, t_col, result))
                else:
                    t_cube = int(t_col/3) + 3* int(row/3)
                    dirty.update([
                        (ROW, t_row),
                        (COL, t_col),
                        (CUBE, t_cube)
                    ])

        while len(new_set):
            t_row, t_col, result = new_set.pop(0)
            self.print_progress(f"solved {t_row},{t_col} handling {row},{col}")
            dirty.update(self.set_cell(t_row, t_col, result))
        return dirty
