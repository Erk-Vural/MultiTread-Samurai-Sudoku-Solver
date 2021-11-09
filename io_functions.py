# I/O
import os


def read_sudoku(file_name):
    grid = []

    with open(file_name, 'r') as file:
        while line := file.readline().rstrip().replace(' ', '').replace('*', '0'):
            matrix_line = []

            for point in line:
                matrix_line.append(int(point))

            grid.append(matrix_line)

    file.close()
    return grid


def check_solution_files_exist(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def save_sudoku_result(y, x, n, file_name):
    f = open(file_name, "a")
    result = "y: " + str(y + 1) + ", " + "x: " + str(x + 1) + ", " + "Value: " + str(n) + "\n"
    f.write(result)
    f.close()


def save_samurai_result(y, x, n, piece_id, starting_point, file_name):
    f = open(file_name, "a")
    result = "piece_id: " + str(piece_id) + " staring point " + str(starting_point) +\
             " y: " + str(y + 1) + ", " + "x: " + str(x + 1) + ", " + "Value: " + str(n) + "\n"
    f.write(result)
    f.close()
