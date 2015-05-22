from itertools import product
from copy import deepcopy


class Sudoku:

    def __init__(self, field):
        """
        Initialize the class with the starting values.
        'field' needs to be a list of 9 lists, each containing 9 numbers.
        0 represents an empty box."""
        self.field = field

    def __str__(self):
        """Allow for nicer printing of the sudoku."""
        return '\n'.join([' '.join([str(__) for __ in _])
                          for _ in self.field]).replace('0', '_') + '\n'

    def in_row(self, row):
        """Return all numbers in a given row."""
        return [_ for _ in self.field[row] if not _ == 0]

    def in_column(self, column):
        """Return all numbers in a given column."""
        return [self.field[i][column] for i in range(9)
                if self.field[i][column] != 0]

    def in_square(self, row, column):
        """
        Takes a coordinate (column, row) and returns all numbers that are
        already in the corresponding square
        """

        # The coordinate of the square we are looking in
        sx = column / 3
        sy = row / 3

        # Read out the square
        result = []
        for x, y in product(range(3*sx, 3*sx+3), range(3*sy, 3*sy+3)):
            result.append(self.field[y][x])

        return [_ for _ in result if not _ == 0]

    def is_faulty(self):
        """
        Check if the sudoku is faulty, i.e. if a number appears twice in
        a row, column or square. Does NOT check if all entries in the field
        are actually numbers. It's not your mom!
        """
        for x, y in product(range(9), range(9)):
            if (len(self.in_row(x)) != len(set(self.in_row(x))) or
               len(self.in_column(y)) != len(set(self.in_column(y))) or
               len(self.in_square(x, y)) != len(set(self.in_square(x, y)))):
                return True
        return False

    def is_solved(self):
        """Checks if the sudoku is solved already."""
        return 0 not in [_ for row in self.field for _ in row]

    def solve(self):
        """Solve the sudoku!"""

        if self.is_faulty():
            print "Can't solve, given sudoku is faulty!"
            return False

        # Remember the field with the least possible options
        # Format: [row, column, number of options, [options]]
        least_options = [0, 0, 9, []]

        # Naive search: Iterate over all fields and see if we can find an empty
        # field whose value is unambiguous because of the numbers of the row,
        # column and square it belongs to.
        while not self.is_solved():

            # Remember the field before we iterate over it
            old_field = self.field

            # Loop over the entire field
            for row, column in product(range(9), range(9)):
                if self.field[row][column] == 0:

                    # Which values are (not) allowed for this field?
                    not_allowed = self.in_row(row) + self.in_column(column) + \
                        self.in_square(row, column)
                    allowed = [_ for _ in range(1, 10) if _ not in not_allowed]

                    # If there is exactly one allowed value, fill that in
                    if len(allowed) == 1:
                        self.field[row][column] = allowed[0]
                    # Otherwise check if this is the field with the least
                    # possible values yet, and if so, remember it
                    elif 1 < len(allowed) < least_options[2]:
                        least_options = [row, column, len(allowed), allowed]

            # If we haven't changed anything in this entire run, stop iterating
            # over the field
            if self.field == old_field:
                break

        # If the sudoku is now solved, we are done!
        if self.is_solved():
            return True
        # Otherwise we will have to start guessing values. We always guess for
        # the field with the minimal number of possible values.
        else:
            x, y = least_options[0], least_options[1]
            # Loop over all possibilities for this field
            for guess in least_options[3]:

                # DeepCopy is necessary because of the recursion, otherwise
                # we might inadvertently modify the field of other instances!
                new_sudoku = Sudoku(deepcopy(self.field))

                # Modify the copied field and try to solve it
                new_sudoku.field[x][y] = guess
                if not new_sudoku.is_faulty():
                    new_sudoku.solve()

                # If we could solve the new sudoku, we are done!
                if new_sudoku.is_solved():
                    self.field = new_sudoku.field
                    break

if __name__ == "__main__":

    sudoku = Sudoku([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 0, 7, 6, 9, 0, 4, 0, 0],
                     [0, 5, 0, 7, 0, 2, 0, 9, 0],
                     [8, 4, 0, 0, 0, 0, 0, 6, 0],
                     [0, 0, 0, 5, 6, 8, 0, 0, 0],
                     [0, 9, 0, 0, 0, 0, 0, 2, 1],
                     [0, 6, 0, 4, 0, 3, 0, 8, 0],
                     [0, 0, 8, 0, 5, 6, 3, 0, 7],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]])

    print sudoku
    sudoku.solve()
    print sudoku
