import concurrent.futures
import threading
import time

are_solved = [[0, False], [1, False], [], [3, False], [4, False]]

threads = [[], [], [], [], []]


def check_block(y, x, grid):
    global are_solved

    if y == 3 and not are_solved[0][1]:
        print("1. part is_solved in puzzle 2\n")
        time.sleep(3)
        are_solved[0][1] = True
        # update_block(0, grid)
        are_solved[1][1] = True
        # update_block(1, grid)
    if y == 8 and x == 8 and not are_solved[3][1]:
        print("2. part is_solved in puzzle 2\n")
        time.sleep(3)
        are_solved[3][1] = True
        # update_block(3, grid)
        are_solved[4][1] = True
        # update_block(4, grid)


def solve(piece_id):
    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    print(str(piece_id) + " is started\n")

    if piece_id == 2:
        for y in range(9):
            for x in range(9):
                check_block(y, x, grid)
                time.sleep(0.1)

        print(str(piece_id) + " is_solved\n")

    else:
        while not are_blocks_solved[piece_id][1]:
            time.sleep(3)
            print(str(piece_id) + " is waiting for is_solved\n")
        if are_blocks_solved[piece_id][1]:
            print(str(piece_id) + " is_solved\n")


if __name__ == "__main__":
    start = time.perf_counter()

    threads = []

    for i in range(5):
        t = threading.Thread(target=solve, args=[i])
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    finish = time.perf_counter()

    print(f'Finished in {round(finish - start, 2)} second(s)')
