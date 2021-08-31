"""GraphicExcel.py."""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import sys
import mplcursors


class GraphicExcel(FigureCanvasQTAgg):
    """Este es el docstring de la funcion."""

    def __init__(self, sheet, club, maxClubs, firstRow):
        """Este es el docstring de la funcion."""
        self.firstRow = firstRow
        self.firstCol = 7
        self.lastCol = 44
        self.gamesPlayed = 20
        self.sheet = sheet
        self.club = club
        self.maxClubs = maxClubs
        self.image = "/home/alvaro/github/LaLigaEstadisticas/real-madrid.png"

        fig = self.printPointsClub()
        super(GraphicExcel, self).__init__(fig)

    def getRowClub(self):
        """."""
        rowClub = self.firstRow
        for value in self.sheet.iter_rows(min_row=self.firstRow,
                                          max_row=self.firstRow
                                          + self.maxClubs - 1,
                                          min_col=5,
                                          max_col=5,
                                          values_only=True):
            if self.club == value[0]:
                return rowClub
            rowClub += 1

        return -1

    def printPointsClub(self):
        """Print points clubs."""
        pointsNew = [None] * self.gamesPlayed
        rangePoints = [None] * self.gamesPlayed
        self.checkGames()
        rowClub = self.getRowClub()

        for value in self.sheet.iter_rows(min_row=rowClub, max_row=rowClub,
                                          min_col=self.firstCol,
                                          max_col=self.lastCol,
                                          values_only=True):
            if self.gamesPlayed == 1:
                points = value[0]
            else:
                points = value[0:self.gamesPlayed]

        print(points)
        self.createLists(points, pointsNew, rangePoints)
        fig = self.createGraphic(pointsNew, rangePoints)

        return fig

    def checkGames(self):
        """Check number of games."""
        if self.gamesPlayed == 1:
            print("Games played is equal to one, can't graphic it")
            sys.exit(1)

    def createLists(self, points, pointsNew, rangePoints):
        """Create lists points and range."""
        temp = 0
        for i in range(0, self.gamesPlayed):
            if points[i] == '-':
                break
            pointsNew[i] = points[i] - 1.5 + temp
            temp = pointsNew[i]
        for j in range(1, self.gamesPlayed + 1):
            rangePoints[j - 1] = j

    def createGraphic(self, pointsNew, rangePoints):
        """Create graphic."""
        plt.rcParams['toolbar'] = 'None'
        fig, ax = plt.subplots(figsize=(10, 2))
        fig.tight_layout()
        fig.patch.set_facecolor('xkcd:gray')
        ax.scatter(rangePoints, pointsNew, color='b')
        lines = ax.plot(rangePoints, pointsNew, color='k')
        ax.set_xlim(0, self.gamesPlayed)
        ax.set_facecolor('xkcd:gray')
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.set_ylabel('Puntuación', fontsize=12)
        ax.set_xlabel('Jornadas', fontsize=12)
        ax.set_title(self.club, fontsize=12)
        ax.grid(linestyle='--', linewidth=0.5)

        def on_add(sel):
            sel.annotation.set_text(
                "Primera parte para el Málaga, Mirandés no atacó. Segunda parte dos tiros muy peligrosos del Mirandés\ny gol anulado por falta inexistente. Gol Mirandés en el 94 con fallo en defensa increíble.\nLo anulan por falta previa inexistente de nuevo. Atraco al Mirandés")
            sel.annotation.get_bbox_patch().set(fc="white", zorder=20, alpha=1)
            sel.annotation.arrow_patch.set(
                arrowstyle="simple", fc="white", alpha=1)

        def mplcursorPoints(lines, ax=None, func=None, **kwargs):
            scats = [ax.scatter(x=line.get_xdata(), y=line.get_ydata(),
                                color='none') for line in lines]
            cursor = mplcursors.cursor(scats, **kwargs)
            if func is not None:
                cursor.connect('add', func)
            return cursor

        mplcursorPoints(
            lines, ax=ax, func=on_add, hover=False)

        return fig
