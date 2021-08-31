import matplotlib.pyplot as plt
import numpy as np
import mplcursors


def create_mplcursor_for_points_on_line(lines, ax=None, annotation_func=None, **kwargs):
    ax = ax or plt.gca()
    scats = [ax.scatter(x=line.get_xdata(), y=line.get_ydata(),
                        color='none') for line in lines]
    cursor = mplcursors.cursor(scats, **kwargs)
    if annotation_func is not None:
        cursor.connect('add', annotation_func)
    return cursor


x = np.arange(10, 301, 10)
y = 30 + np.random.randint(-5, 6, x.size).cumsum()

fig, ax = plt.subplots()
lines = ax.plot(x, y)
cursor = create_mplcursor_for_points_on_line(lines, ax=ax, hover=True)

plt.show()
