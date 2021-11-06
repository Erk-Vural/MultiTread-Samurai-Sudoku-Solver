import matplotlib.pyplot as plt


# Graphs
# Currently it's almost what we want

def get_unique_numbers(numbers):
    list_of_unique_numbers = []

    unique_numbers = set(numbers)

    for number in unique_numbers:
        list_of_unique_numbers.append(number)

    return list_of_unique_numbers


def plot_sudoku_graph(times, results):
    # y - Square Found
    y = get_unique_numbers(results)
    # x - time
    jump_time = (len(times) // len(y)) + 1
    x = times[::jump_time]

    plt.plot(x, y)

    plt.yticks(y[::10])
    plt.xticks(x[::10])

    plt.xlabel('x - time')
    plt.ylabel('y - Square Found')
    plt.title('9x9 Sudoku Time-Found Graph')

    plt.show()
