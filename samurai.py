import sys

import numpy as np
import threading

import pygame

from io_functions import read_sudoku, check_solution_files_exist, save_samurai_result
from timer import Timer

# GUI
black = (0, 0, 0)
light_gray = (230, 230, 230)

block_amount = 21
block_size = 40

WINDOW_HEIGHT = block_size * block_amount
WINDOW_WIDTH = block_size * block_amount


def draw_grid(grid):
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            if grid[y // block_size][x // block_size] == -1:
                continue

            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(SCREEN, black, rect, 2)

            value = str(grid[y // block_size][x // block_size])
            set_number(x, y, value)

    pygame.display.update()


def set_number(x, y, n):
    # Displays a number on point
    font = pygame.font.SysFont('arial', block_size)
    text = font.render(n, True, (0, 0, 0))
    SCREEN.blit(text, (x, y))


# Samurai
# Solves samurai examples without treads, with 5 treads and 10 treads 10 tread version has 2 thread on same puzzle and
# starts from 2 different points

samurai_example_file_name = "examples/samurai.txt"
samurai_solved_file_name = "solved/samurai(result).txt"

is_puzzle_solved = [False, False, False, False, False]

t = Timer()

# samurai_grid is the version read from file
# puzzle[0] is top_left
# puzzle[1] is top_right
# puzzle[2] is middle
# puzzle[3] is bottom_left
# puzzle[4] is bottom_right
samurai_grid = []
samurai_matrix = []

puzzles = [[], [], [], [], []]
solved_puzzles = [[], [], [], [], []]


# Adds spaces to samurai list to turn it to matrix
def samurai_list_to_matrix():
    global samurai_matrix

    samurai_matrix = samurai_grid

    for y in range(21):
        if y < 6 or y > 14:
            for x in range(3):
                samurai_matrix[y].insert(9 + x, -1)
        if 8 < y < 12:
            for x in range(6):
                samurai_matrix[y].insert(x, -1)
                samurai_matrix[y].append(-1)


# Takes samurai_sudoku list and separate it to 5 list pieces then to matrices
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
        puzzles[i] = list_to_matrix(temp_puzzles[i], 9)
        print(np.matrix(puzzles[i]))
        print("\n")


# Convert puzzle lists to puzzle matrices
def list_to_matrix(old_list, width):
    new_matrix = []
    matrix_line = []

    for x in range(width * width):
        matrix_line.append(old_list[x])

        if x % width == width - 1 and x > width - 1 or x == width - 1:
            new_matrix.append(matrix_line)
            matrix_line = []

    return new_matrix


# Checks if value is suitable for point and if point is at one of the conflicted block checks both puzzles
def check(y, x, n, grid, piece_id):
    add_to_x = 0
    add_to_y = 0
    check_piece_id = piece_id

    # Solve middle with other corners in mind
    if piece_id == 2:
        # left
        if 0 <= x < 3:
            # top_left
            if 0 <= y < 3:
                add_to_x = 6
                add_to_y = 6
                check_piece_id = 0
            # bottom_left
            if 6 <= y < 9:
                add_to_x = 6
                add_to_y = -6
                check_piece_id = 3
        # right
        if 6 <= x < 9:
            # top_right
            if 0 <= y < 3:
                add_to_x = -6
                add_to_y = 6
                check_piece_id = 1
            # bottom_right
            if 6 <= y < 9:
                add_to_x = -6
                add_to_y = -6
                check_piece_id = 4

    return possible(y, x, n, grid) \
           and possible(y + add_to_y, x + add_to_x, n, puzzles[check_piece_id]) \
           and not is_puzzle_solved[piece_id]


# Checks col, row and block to determine if value is suitable for point
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


# After middle puzzle is solved function updates all puzzle's conflicted blocks
def update_puzzles(piece_id, starting_point, grid):
    global puzzles

    if piece_id == 0:
        for y in range(3):
            for x in range(3):
                puzzles[piece_id][y + 6][x + 6] = grid[y][x]
    if piece_id == 1:
        for y in range(3):
            for x in range(6, 9):
                puzzles[piece_id][y + 6][x - 6] = grid[y][x]
    if piece_id == 3:
        for y in range(6, 9):
            for x in range(3):
                puzzles[piece_id][y - 6][x + 6] = grid[y][x]
    if piece_id == 4:
        for y in range(6, 9):
            for x in range(6, 9):
                puzzles[piece_id][y - 6][x - 6] = grid[y][x]

    print("Updated version of: " + str(piece_id) + ", " + str(starting_point))
    print(np.matrix(puzzles[piece_id]))
    print("\n")


# Using recursion to solve examples.
# Function search for an empty point then tries all values between (1,9), if suitable
# value found, it replaces point with value and calls a new solve. If a solve returns
# it means that there is no suitable value for the point, therefore previous point
# assignment is false because the next point can't be found.Program returns to  previous
# solve and replace point with 0 (empty) and search for a new possible value.
# If a new suitable value founds a new solve called otherwise current solve return too
# and previous point is reassigned.
# Function works until all grid is solved.then prints solved grid
def solve(piece_id, starting_point):
    global is_puzzle_solved
    global t
    global solved_puzzles

    grid = puzzles[piece_id]

    head_point = 0
    end_point = 9
    operation = 1

    # If starting point is 2 loops start from reverse
    if starting_point == 2:
        head_point = 8
        end_point = -1
        operation = -1

    for y in range(head_point, end_point, operation):
        for x in range(head_point, end_point, operation):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if check(y, x, n, grid, piece_id):
                        grid[y][x] = n

                        save_samurai_result(y, x, n, piece_id, starting_point, samurai_solved_file_name)

                        solve(piece_id, starting_point)

                        grid[y][x] = 0

                        save_samurai_result(y, x, 0, piece_id, starting_point, samurai_solved_file_name)

                return

    for y in range(9):
        matrix_line = []
        for x in range(9):
            matrix_line.append(grid[y][x])
        solved_puzzles[piece_id].append(matrix_line)

    print("Final version of: " + str(piece_id))
    print(np.matrix(solved_puzzles[piece_id]))
    print("\n")

    is_puzzle_solved[piece_id] = True


# Solve samurai without threads starting from middle puzzle then loops through other corners
def solve_samurai():
    solve(2, 1)

    for i in range(5):
        if i == 2:
            continue
        update_puzzles(i, 1, solved_puzzles[2])
        solve(i, 1)


# Solve samurai with threads corners wait until middle puzzle is solved than other corners start at same time
# In 10 tread version loop is same with 5 tread but inside it loops 2 times and creates 10 treads, treads belongs to
# same puzzle starts after one another. Some times one tread can solve all puzzle by itself might be improved later
def solve_samurai_tread(starting_points):
    threads = []

    for i in range(5):
        for starting_point in starting_points:
            trd = threading.Thread(target=manage_treads, args=[i, starting_point])
            trd.start()
            threads.append(trd)

    for thread in threads:
        thread.join()


# Other treads waits until middle puzzle solved then updates blocks and start solving
def manage_treads(piece_id, starting_point):
    print(str(piece_id) + ", " + str(starting_point) + " is started\n")

    if piece_id == 2:
        solve(piece_id, starting_point)
    else:
        while not is_puzzle_solved[2]:
            print(str(piece_id) + ", " + str(starting_point) + " is waiting\n")
            pass
        if is_puzzle_solved[2]:
            update_puzzles(piece_id, starting_point, solved_puzzles[2])
            solve(piece_id, starting_point)


def main():
    global samurai_grid
    global samurai_example_file_name
    global samurai_solved_file_name

    samurai_example_file_name = "examples/samurai.txt"
    samurai_solved_file_name = "solved/samurai(result).txt"

    # Create window
    global SCREEN

    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(light_gray)

    samurai_grid = read_sudoku(samurai_example_file_name)
    print("Read Version: ")
    print(samurai_grid)
    print("\n")

    check_solution_files_exist(samurai_solved_file_name)

    convert_to_pieces()

    samurai_list_to_matrix()
    draw_grid(samurai_matrix)

    tread_type1 = [1]  # 5 tread 1 starting point
    tread_type2 = [1, 2]  # 10 tread 2 starting point

    t.start()

    # solve_samurai()
    # solve_samurai_tread(tread_type1)

    t.stop()

    # Quit button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
