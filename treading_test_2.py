import concurrent.futures
import threading
import time

is_solved = False


def check_block(piece_id):
    pass


def solve(piece_id):
    if piece_id == 2:
        for y in range(9):
            for x in range(9):
                if y == 2 and x == 2:
                    pass



if __name__ == "__main__":
    start = time.perf_counter()

    finish = time.perf_counter()

    print(f'Finished in {round(finish - start, 2)} second(s)')
