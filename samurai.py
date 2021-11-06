import numpy as np

from file_functions import read_sudoku, check_solution_files_exist
from timer import Timer

# Samurai
sudoku_type = 2
is_solved = False

t = Timer()

samurai_grid = []

puzzle_top_left = []
puzzle_top_right = []
puzzle_middle = []
puzzle_bottom_left = []
puzzle_bottom_right = []


def list_to_matrix(puzzle_list):
    puzzle_matrix = []
    matrix_line = []

    for x in range(81):
        matrix_line.append(puzzle_list[x])

        if x % 9 == 8 and x > 8 or x == 8:
            puzzle_matrix.append(matrix_line)
            matrix_line = []
    return puzzle_matrix


def convert_to_pieces():
    global puzzle_top_left
    global puzzle_top_right
    global puzzle_middle
    global puzzle_bottom_left
    global puzzle_bottom_right

    # temp lists
    top_left = []
    top_right = []
    middle = []
    bottom_left = []
    bottom_right = []

    y_range = len(samurai_grid)
    for y in range(y_range):
        x_range = len(samurai_grid[y])
        for x in range(x_range):
            if y < 6:
                if x < 9:
                    top_left.append(samurai_grid[y][x])
                if x >= 9:
                    top_right.append(samurai_grid[y][x])

            if 6 <= y < 9:
                if x < 9:
                    top_left.append(samurai_grid[y][x])
                if 6 <= x < 15:
                    middle.append(samurai_grid[y][x])
                if x >= 12:
                    top_right.append(samurai_grid[y][x])

            if 9 <= y < 12:
                middle.append(samurai_grid[y][x])

            if 12 <= y < 15:
                if x < 9:
                    bottom_left.append(samurai_grid[y][x])
                if 6 <= x < 15:
                    middle.append(samurai_grid[y][x])
                if x >= 12:
                    bottom_right.append(samurai_grid[y][x])

            if y >= 15:
                if x < 9:
                    bottom_left.append(samurai_grid[y][x])
                if x >= 9:
                    bottom_right.append(samurai_grid[y][x])

    puzzle_top_left = list_to_matrix(top_left)
    print(np.matrix(puzzle_top_left))
    print("\n")
    puzzle_top_right = list_to_matrix(top_right)
    print(np.matrix(puzzle_top_right))
    print("\n")
    puzzle_middle = list_to_matrix(middle)
    print(np.matrix(puzzle_middle))
    print("\n")
    puzzle_bottom_left = list_to_matrix(bottom_left)
    print(np.matrix(puzzle_bottom_left))
    print("\n")
    puzzle_bottom_right = list_to_matrix(bottom_right)
    print(np.matrix(puzzle_bottom_right))
    print("\n")


def possible(y, x, n, grid):
    # Check col
    for i in range(0, 9):
        if grid[y][i] == n:
            return False
    # Check row
    for i in range(0, 9):
        if grid[i][x] == n:
            return False
    # Check block
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0 + i][x0 + j] == n:
                return False
    # if number is not used before return true
    return True


# Using recursion to solve sudoku.
# Function search for an empty point then tries all values between (1,9), if suitable
# value found, it replaces point with value and calls a new solve. If a solve returns
# it means that there is no suitable value for the point, therefore previous point
# assignment is false because the next point can't be found.Program returns to  previous
# solve and replace point with 0 (empty) and search for a new possible value.
# If a new suitable value founds a new solve called otherwise current solve return too
# and previous point is reassigned.
# Function works until all grid is solved.then prints solved grid
def solve(grid):
    global is_solved

    global t

    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n, grid) and not is_solved:
                        grid[y][x] = n

                        solve(grid)

                        grid[y][x] = 0

                return

    print("Final version: ")
    print(np.matrix(grid))
    print("\n")

    is_solved = True


def main():
    global samurai_grid
    global is_solved

    samurai_grid = read_sudoku(sudoku_type)
    print("Read Version: ")
    print(samurai_grid)
    print("\n")

    check_solution_files_exist(sudoku_type)

    convert_to_pieces()

    solve(puzzle_top_left)
    is_solved = False
    solve(puzzle_top_right)
    is_solved = False
    solve(puzzle_middle)
    is_solved = False
    solve(puzzle_bottom_left)
    is_solved = False
    solve(puzzle_bottom_right)
    is_solved = False


if __name__ == "__main__":
    main()
