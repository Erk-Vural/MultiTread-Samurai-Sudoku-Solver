import pygame as pygame
import sys

from file_functions import *
from graphs import plot_sudoku_graph
from timer import Timer

# GUI
black = (0, 0, 0)
light_gray = (230, 230, 230)

block_amount = 9
block_size = 60

WINDOW_HEIGHT = block_size * block_amount
WINDOW_WIDTH = block_size * block_amount


def set_number(x, y, n):
    # Displays a number on point
    font = pygame.font.SysFont('arial', block_size)
    text = font.render(n, True, (0, 0, 0))
    SCREEN.blit(text, (x, y))


def clear_rect(x, y):
    rect = pygame.Rect(x, y, block_size, block_size)
    SCREEN.fill(light_gray, rect)
    pygame.draw.rect(SCREEN, black, rect, 1)


def draw_grid():
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(SCREEN, black, rect, 1)

            value = str(puzzle[y // block_size][x // block_size])
            set_number(x, y, value)

    pygame.display.update()


def update_point(y, x, n):
    x0 = x * block_size
    y0 = y * block_size

    clear_rect(x0, y0)

    # time.sleep(0.01)

    set_number(x0, y0, str(n))
    pygame.display.update()


# Sudoku
# Checks row col and block to confirm "n" is available for selected point
sudoku_type = 1
is_solved = False

t = Timer()

puzzle = []

times = []
results = []


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

                        times.append(t.get_current_time())
                        # save result to plot graph but save method is fouled, it should save each solved point
                        results.append((y + 1) * 10 + (x + 1))

                        save_sudoku_result(y, x, n, sudoku_type)
                        update_point(y, x, n)

                        solve(grid)

                        grid[y][x] = 0

                        save_sudoku_result(y, x, 0, sudoku_type)

                return

    print("Final version: ")
    print(np.matrix(grid))
    print("\n")

    is_solved = True
    t.stop()

    plot_sudoku_graph(times, results)


def main():
    global puzzle

    # Create window
    global SCREEN

    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(light_gray)

    puzzle = read_sudoku(sudoku_type)

    # testing top_left
    puzzle = [[0, 0, 5, 7, 0, 0, 0, 2, 0],
              [4, 9, 0, 0, 6, 0, 0, 1, 0],
              [0, 0, 7, 0, 0, 4, 9, 0, 6],
              [0, 0, 6, 0, 0, 0, 0, 0, 8],
              [0, 7, 0, 0, 0, 0, 0, 9, 0],
              [2, 0, 0, 0, 0, 0, 3, 0, 0],
              [5, 0, 8, 9, 0, 0, 7, 3, 1],
              [0, 1, 0, 0, 3, 0, 2, 8, 5],
              [0, 2, 0, 0, 0, 5, 6, 4, 9]]

    print("Read Version: ")
    print(np.matrix(puzzle))
    print("\n")

    check_solution_files_exist(sudoku_type)

    draw_grid()

    t.start()
    solve(puzzle)

    # Quit button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
