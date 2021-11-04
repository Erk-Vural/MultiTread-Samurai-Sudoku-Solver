import numpy as np
from timer import Timer

grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]

print(np.matrix(grid))


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
                        solve()
                        grid[y][x] = 0

                return


    print(np.matrix(grid))
    t.stop()
    input("More?")  # Checks if other answers are available

solve()