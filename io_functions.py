# I/O
import os

import numpy as np


def check_solution_files_exist(sudoku_type):
    file_name = ""
    if sudoku_type == 1:
        file_name = "./examples/solved/9x9(result).txt"
    if sudoku_type == 2:
        file_name = "./examples/solved/samurai(result).txt"

    if os.path.exists(file_name):
        os.remove(file_name)


def save_sudoku_result(y, x, n, sudoku_type):
    file_name = ""
    if sudoku_type == 1:
        file_name = "./examples/solved/9x9(result).txt"
    if sudoku_type == 2:
        file_name = "./examples/solved/samurai(result).txt"

    f = open("./examples/solved/9x9(result).txt", "a")
    f.write("y: " + str(y + 1) + ", " + "x: " + str(x + 1) + ", " + "Value: " + str(n))
    f.write("\n")
    f.close()


def read_sudoku(sudoku_type):
    file_name = ""
    if sudoku_type == 1:
        file_name = './examples/sudoku/9x9.txt'
    if sudoku_type == 2:
        file_name = './examples/sudoku/samurai.txt'

    grid = []

    with open(file_name, 'r') as file:
        while line := file.readline().rstrip().replace(' ', '').replace('*', '0'):
            matrix_line = []

            for point in line:
                matrix_line.append(int(point))

            grid.append(matrix_line)

    file.close()
    return grid
