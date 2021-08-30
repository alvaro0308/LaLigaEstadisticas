import string
import matplotlib.pyplot as plt
import mplcursors
fig, ax = plt.subplots()
ax.bar(range(9), range(1, 10), align="center", zorder=10)
labels = string.ascii_uppercase[:9]
ax.set(xticks=range(9), xticklabels=labels, title="Hover over a bar")

cursor = mplcursors.cursor(hover=False)


@cursor.connect("add")
def on_add(sel):
    x, y, width, height = sel.artist[sel.target.index].get_bbox().bounds
    sel.annotation.set(text=f"{x+width/2}: {height}",
                       position=(0, -20), anncoords="offset points")
    sel.annotation.xy = (x + width / 2, y + height)
    sel.annotation.get_bbox_patch().set(fc="white", zorder=20, alpha=1)
    sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=1)


plt.show()
