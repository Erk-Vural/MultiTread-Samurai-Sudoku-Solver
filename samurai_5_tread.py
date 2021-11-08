import numpy as np
import threading
import time

from file_functions import read_sudoku, check_solution_files_exist
from sudoku import possible
from timer import Timer

# Samurai
sudoku_type = 2
are_blocks_solved = [[0, False], [1, False], [2, False], [3, False], [4, False]]
are_puzzles_solved = [[0, False], [1, False], [2, False], [3, False], [4, False]]

t = Timer()

# samurai_grid is the version read from file
# puzzle[0] is top_left
# puzzle[1] is top_right
# puzzle[2] is middle
# puzzle[3] is bottom_left
# puzzle[4] is bottom_right
samurai_grid = []
puzzles = [[], [], [], [], []]
solved_puzzles = [[], [], [], [], []]


# Convert puzzle lists to puzzle matrices
def list_to_matrix(puzzle_list):
    puzzle_matrix = []
    matrix_line = []

    for x in range(81):
        matrix_line.append(puzzle_list[x])

        if x % 9 == 8 and x > 8 or x == 8:
            puzzle_matrix.append(matrix_line)
            matrix_line = []
    return puzzle_matrix


# Separates puzzles to different lists
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


# Checks if value is suitable for point if point is at one of the conflicted block checks
# both puzzles
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
           and not are_puzzles_solved[piece_id][1]


def check_block(y, x, grid):
    global are_blocks_solved

    if y == 3 and not are_blocks_solved[0][1]:
        print("1. part is_solved in puzzle 2\n")

        are_blocks_solved[0][1] = True
        update_puzzles(0, grid)
        are_blocks_solved[1][1] = True
        update_puzzles(1, grid)
    if y == 8 and x == 8 and not are_blocks_solved[3][1]:
        print("2. part is_solved in puzzle 2\n")

        are_blocks_solved[3][1] = True
        update_puzzles(3, grid)
        are_blocks_solved[4][1] = True
        update_puzzles(4, grid)


def solve_5_tread(piece_id):
    global are_blocks_solved
    global t
    global solved_puzzles

    if piece_id == 2:
        grid = puzzles[piece_id]

        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    for n in range(1, 10):
                        if check(y, x, n, grid, piece_id):
                            grid[y][x] = n

                            check_block(y, x, grid)

                            solve_5_tread(piece_id)

                            grid[y][x] = 0

                    return

    else:
        while not are_blocks_solved[piece_id][1]:
            pass
        if are_blocks_solved[piece_id][1]:
            grid = puzzles[piece_id]

            for y in range(9):
                for x in range(9):
                    if grid[y][x] == 0:
                        for n in range(1, 10):
                            if check(y, x, n, grid, piece_id):
                                check_block(y, x, grid)

                                grid[y][x] = n

                                solve_5_tread(piece_id)

                                grid[y][x] = 0

                        return

    for y in range(9):
        matrix_line = []
        for x in range(9):
            matrix_line.append(grid[y][x])
        solved_puzzles[piece_id].append(matrix_line)
        matrix_line = []

    print("Final version of: " + str(piece_id))
    print(np.matrix(solved_puzzles[piece_id]))
    print("\n")

    are_puzzles_solved[piece_id][1] = True


# After middle is solved function updates all puzzles
def update_puzzles(piece_id, grid):
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

    print("Updated version of: " + str(piece_id))
    print(np.matrix(puzzles[piece_id]))
    print("\n")


# Solve samurai without threads starting from middle puzzle
def solve_samurai_tread():
    threads = []

    for i in range(5):
        trd = threading.Thread(target=solve_5_tread, args=[i])
        trd.start()
        threads.append(trd)

    for thread in threads:
        thread.join()


def main():
    global samurai_grid

    samurai_grid = read_sudoku(sudoku_type)
    print("Read Version: ")
    print(samurai_grid)
    print("\n")

    check_solution_files_exist(sudoku_type)

    convert_to_pieces()

    solve_samurai_tread()


if __name__ == "__main__":
    main()