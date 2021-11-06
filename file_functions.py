# I/O
import os

import numpy as np


def check_solution_files_exist():
    if os.path.exists("./examples/solved/9x9(result).txt"):
        os.remove("./examples/solved/9x9(result).txt")


def save_sudoku_result(y, x, n):

    f = open("./examples/solved/9x9(result).txt", "a")
    f.write("y: " + str(y + 1) + ", " + "x: " + str(x + 1) + ", " + "Value: " + str(n))
    f.write("\n")
    f.close()


def read_sudoku():
    grid = []

    with open('./examples/sudoku/9x9.txt', 'r') as file:
        while line := file.readline().rstrip().replace(' ', '').replace('*', '0'):
            matrix_line = []

            for point in line:
                matrix_line.append(int(point))

            grid.append(matrix_line)

        print("Read Version: ")
        print(np.matrix(grid))
        print("\n")

    file.close()
    return grid
