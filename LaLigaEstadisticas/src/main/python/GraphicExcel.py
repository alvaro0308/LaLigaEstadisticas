"""GraphicExcel.py."""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import sys


class GraphicExcel(FigureCanvasQTAgg):
    """Este es el docstring de la funcion."""

    def __init__(self, sheet, club, maxClubs, firstRow):
        """Este es el docstring de la funcion."""
        self.firstRow = firstRow
        self.firstCol = 7
        self.lastCol = 44
        self.gamesPlayed = 38
        self.sheet = sheet
        self.club = club
        self.maxClubs = maxClubs

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

        # print(points)
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
        ax.plot(rangePoints, pointsNew, color='k')
        ax.set_xlim(0, self.gamesPlayed)
        ax.set_facecolor('xkcd:gray')
        ax.set_yticklabels([])
        ax.set_ylabel('Puntuación', fontsize=10)
        ax.set_xlabel('Jornadas', fontsize=10)
        ax.set_title('Club\n')
        ax.grid(linestyle='--', linewidth=0.5)
        # plt.show()

        return fig
