
from file_functions import read_sudoku
from timer import Timer

# Samurai
sudoku_type = 2
is_solved = False

t = Timer()

grid = []


def main():
    global grid

    grid = read_sudoku(sudoku_type)
    print("Read Version: ")
    print(grid)
    print("\n")


if __name__ == "__main__":
    main()
