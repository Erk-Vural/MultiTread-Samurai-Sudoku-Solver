import matplotlib.pyplot as plt


# Graphs

def plot_sudoku_graph(times, points):
    # y - Square Found
    y = points
    # x - time
    jump_time = (len(times) // len(y))
    x = times[::jump_time]

    while not len(x) == len(y):
        if len(x) > len(y):
            x.pop(0)
        else:
            x.append(times[-1])
            times.pop(-1)

    plt.plot(x, y)

    plt.yticks(y[::15])
    plt.xticks(x[::25])

    plt.xlabel('x - time')
    plt.ylabel('y - Square Found')
    plt.title('9x9 Sudoku Time-Found Graph')

    plt.show()
