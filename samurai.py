import numpy as np

from file_functions import read_sudoku, check_solution_files_exist
from sudoku import possible
from timer import Timer

# Samurai
sudoku_type = 2
is_solved = False

t = Timer()

# samurai_grid is the version read from file
# puzzle[0] is top_left
# puzzle[1] is top_right
# puzzle[2] is middle
# puzzle[3] is bottom_left
# puzzle[4] is bottom_right
samurai_grid = []
puzzles = [[], [], [], [], []]


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
    global puzzles

    # temp puzzle lists
    temp_puzzles = [[], [], [], [], []]

    y_range = len(samurai_grid)
    for y in range(y_range):
        x_range = len(samurai_grid[y])
        for x in range(x_range):
            if y < 6:
                if x < 9:
                    temp_puzzles[0].append(samurai_grid[y][x])
                if x >= 9:
                    temp_puzzles[1].append(samurai_grid[y][x])

            if 6 <= y < 9:
                if x < 9:
                    temp_puzzles[0].append(samurai_grid[y][x])
                if 6 <= x < 15:
                    temp_puzzles[2].append(samurai_grid[y][x])
                if x >= 12:
                    temp_puzzles[1].append(samurai_grid[y][x])

            if 9 <= y < 12:
                temp_puzzles[2].append(samurai_grid[y][x])

            if 12 <= y < 15:
                if x < 9:
                    temp_puzzles[3].append(samurai_grid[y][x])
                if 6 <= x < 15:
                    temp_puzzles[2].append(samurai_grid[y][x])
                if x >= 12:
                    temp_puzzles[4].append(samurai_grid[y][x])

            if y >= 15:
                if x < 9:
                    temp_puzzles[3].append(samurai_grid[y][x])
                if x >= 9:
                    temp_puzzles[4].append(samurai_grid[y][x])

    for i in range(5):
        puzzles[i] = list_to_matrix(temp_puzzles[i])
        print(np.matrix(puzzles[i]))
        print("\n")


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

    for i in range(5):
        solve(puzzles[i])
        is_solved = False


if __name__ == "__main__":
    main()
