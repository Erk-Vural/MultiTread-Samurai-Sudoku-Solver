import sys
import numpy as np
import pygame as pygame
import os
import time

from timer import Timer

grid = []

# GUI
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 540
WINDOW_WIDTH = 540
block_size = WINDOW_HEIGHT // 9  # Set the size of the grid block


def set_text(x, y, n):
    # Displays a number on that tile
    font = pygame.font.SysFont('arial', block_size)
    text = font.render(n, True, (0, 0, 0))
    SCREEN.blit(text, (x, y))


def clear_rect(x, y):
    rect = pygame.Rect(x, y, block_size, block_size)
    SCREEN.fill(WHITE, rect)
    pygame.draw.rect(SCREEN, BLACK, rect, 1)


def draw_grid():
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

            value = str(grid[y // block_size][x // block_size])
            set_text(x, y, value)

    pygame.display.update()


def update_grid(y, x, n):
    x0 = x * block_size
    y0 = y * block_size

    clear_rect(x0, y0)

    time.sleep(0.01)

    set_text(x0, y0, str(n))
    pygame.display.update()


# I/O
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


# Sudoku
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
                        update_grid(y,x,n)

                        solve()
                        grid[y][x] = 0


                return

    print("Final version: ")
    print(np.matrix(grid))
    print("\n")

    t.stop()
    # input("More?")  # Checks if other answers are available


def main():
    # Create window
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(WHITE)

    read_matrix()
    check_file_exist()
    draw_grid()
    solve()

    # Quit button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


main()
