import matplotlib.pyplot as plt


# Graphs
# Currently we use all calculation vs all time but it should be point solved vs time


def plot_sudoku_graph(times, results):
    # x - time
    times.sort()
    x = times
    # y - Square Found

    results.sort()
    y = results

    plt.plot(x, y)

    plt.xticks(times[::800])

    plt.xlabel('x - time')
    plt.ylabel('y - Square Found')
    plt.title('9x9 Sudoku Time-Found Graph')

    plt.show()



