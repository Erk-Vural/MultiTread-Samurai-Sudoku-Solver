import numpy as np
from timer import Timer
import os


grid = []


def check_file_exist():
    if os.path.exists("./examples/solved/9x9(solved).txt"):
        os.remove("./examples/solved/9x9(solved).txt")


def write_results(y, x, n):
    f = open("./examples/solved/9x9(solved).txt", "a")
    f.write(str(y + 1) + ", " + str(x + 1) + ", " + str(n))
    f.write("\n")
    f.close()


def read_matrix():
    global grid

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


# Checks row col and block to confirm "n" is available
def possible(y, x, n):
    global grid
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
def solve():
    t = Timer()
    t.start()

    global grid

    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        grid[y][x] = n

                        write_results(y, x, n)

                        solve()
                        grid[y][x] = 0

                return

    print("Final version: ")
    print(np.matrix(grid))
    print("\n")

    t.stop()
    input("More?")  # Checks if other answers are available


read_matrix()
check_file_exist()
solve()
