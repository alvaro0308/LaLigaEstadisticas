import matplotlib.pyplot as plt
import numpy as np
import mplcursors
np.random.seed(42)

fig, ax = plt.subplots()
ax.scatter(*np.random.random((2, 26)))
ax.set_title("Mouse over a point")
cursor = mplcursors.cursor(ax, hover=True)


@cursor.connect("add")
def on_add(sel):
    sel.annotation.get_bbox_patch().set(fc="white", zorder=20, alpha=1)
    sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=1)


plt.show()
