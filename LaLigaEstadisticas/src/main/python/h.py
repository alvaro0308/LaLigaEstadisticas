# -*- coding: iso-8859-1 -*-#
#!/usr/bin/env python
# The following allows special characters to be in comments (e.g. the extended Swedish alphabet)
# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
# For setting size and position of matplotlib figure
import matplotlib
matplotlib.use("WXAgg")


class Cursor(object):
    """
     Purpose: Define a cursor whose interesection will track points along a curve
    """

    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(color='k', linewidth=0.25)  # the horiz line
        self.ly = ax.axvline(color='k', linewidth=0.25)  # the vert line

        # Text location in data coords
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.4)
        self.txt = self.ax.text(0, 0, '', fontsize=8, bbox=props)

    def mouse_move(self, event):
        '''
         Purpose: respond to movement of the mouse
        '''
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        self.txt.set_position((x, y))
        # Update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()


class SnaptoCursor(object):
    """
    Like Cursor but the current center of the crosshair at (x,y) will snap to the nearest
    (x,y) on the curve.
    For simplicity, I'm assuming x is sorted
    """

    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.x = x
        self.y = y

        # Text location in data coords
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.4)
        self.txt = self.ax.text(0, 0, '', fontsize=8, bbox=props)

    def mouse_move(self, event):
        """
         Purpose: Track the movement of the mouse coords and then update the position
                  of the intersection of the cursor cross-hairs
        """
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata       # x,y coordinates of mouse

        self.txt.set_position((x, y))

        # Find closest pt on data curve to (x,y) of cross-air intersection
        indx = min(np.searchsorted(self.x, [x])[0], len(self.x) - 1)
        x = self.x[indx]
        y = self.y[indx]
        # Update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)
        # place a text box in upper left in axes coords
        # self.ax.text(x, y, 'test', transform=ax.transAxes, fontsize=8,
        #        verticalalignment='top', bbox=props)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        print('x=%1.2f, y=%1.2f' % (x, y))
        self.ax.figure.canvas.draw_idle()


t = np.arange(0.0, 1.0, 0.01)
s = np.sin(2 * 2 * np.pi * t)
fig, ax = plt.subplots(figsize=(14, 7.5))
fig.canvas.set_window_title('TS with tracking cursor')

# cursor = Cursor(ax)
cursor = SnaptoCursor(ax, t, s)
plt.connect('motion_notify_event', cursor.mouse_move)

ax.plot(t, s, 'o')

plt.axis([0, 1, -1, 1])
plt.grid(axis='both')
plt.show()
