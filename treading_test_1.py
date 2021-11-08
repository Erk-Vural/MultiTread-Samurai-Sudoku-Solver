import concurrent.futures
import threading
import time

is_solved = False


def do_something(piece_id):
    global is_solved

    print(str(piece_id) + " is started\n")
    if piece_id == 2:
        time.sleep(3)
        is_solved = True
        print(str(piece_id) + " is finished\n")
    else:
        while not is_solved:
            time.sleep(3)
            print(str(piece_id) + " is waiting for is_solved\n")
        if is_solved:
            print(str(piece_id) + " is_solved\n")
            # is_solved = False


if __name__ == "__main__":
    start = time.perf_counter()

    puzzles = []

    for i in range(5):
        t = threading.Thread(target=do_something, args=[i])
        t.start()
        puzzles.append(t)

    for thread in puzzles:
        thread.join()

    finish = time.perf_counter()

    print(f'Finished in {round(finish - start, 2)} second(s)')
