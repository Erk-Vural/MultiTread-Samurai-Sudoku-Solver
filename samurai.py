import numpy as np

from file_functions import read_sudoku, check_solution_files_exist
from timer import Timer

# Samurai
sudoku_type = 2
is_solved = False

t = Timer()

grid = []

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

    y_range = len(grid)
    for y in range(y_range):
        x_range = len(grid[y])
        for x in range(x_range):
            if y < 6:
                if x < 9:
                    top_left.append(grid[y][x])
                if x >= 9:
                    top_right.append(grid[y][x])

            if 6 <= y < 9:
                if x < 9:
                    top_left.append(grid[y][x])
                if 6 <= x < 15:
                    middle.append(grid[y][x])
                if x >= 12:
                    top_right.append(grid[y][x])

            if 9 <= y < 12:
                middle.append(grid[y][x])

            if 12 <= y < 15:
                if x < 9:
                    bottom_left.append(grid[y][x])
                if 6 <= x < 15:
                    middle.append(grid[y][x])
                if x >= 12:
                    bottom_right.append(grid[y][x])

            if y >= 15:
                if x < 9:
                    bottom_left.append(grid[y][x])
                if x >= 9:
                    bottom_right.append(grid[y][x])

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


def main():
    global grid

    grid = read_sudoku(sudoku_type)
    print("Read Version: ")
    print(grid)
    print("\n")

    check_solution_files_exist(sudoku_type)

    convert_to_pieces()


if __name__ == "__main__":
    main()
