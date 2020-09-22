"""Graphic."""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys


class GraphicExcel(FigureCanvasQTAgg):
    def __init__(self, sheet):
        # fig = Figure(figsize=(5, 4), dpi=100)
        # self.axes = fig.add_subplot(111)
        # super(GraphicExcel, self).__init__(fig)
        maxClubsSantander = 20
        maxClubsSmartbank = 22
        firstRowSantander = 3
        firstRowSmartbank = 25
        firstCol = 7
        lastCol = 44

        gamesPlayed = 38

        print("Liga Santander")
        fig = self.printPoints(sheet, firstRowSantander, firstCol,
                               lastCol, maxClubsSantander, gamesPlayed)

        super(GraphicExcel, self).__init__(fig)

    def printPoints(self, sheet, firstRow, firstCol, lastCol, maxClubs, gamesPlayed):
        """Print points clubs."""
        pointsNew = [None] * gamesPlayed
        rangePoints = [None] * gamesPlayed
        for row in range(firstRow, maxClubs + firstRow):
            for value in sheet.iter_rows(min_row=row, max_row=row,
                                         min_col=firstCol, max_col=lastCol,
                                         values_only=True):
                if gamesPlayed == 1:
                    points = value[0]
                else:
                    points = value[0:gamesPlayed]

                # print(points)
                self.checkGames(gamesPlayed)
                self.createLists(points, pointsNew, rangePoints, gamesPlayed)
                fig = self.createGraphic(pointsNew, rangePoints, gamesPlayed)

        return fig

    def checkGames(self, gamesPlayed):
        """Check number of games."""
        if gamesPlayed == 1:
            print("Games played is equal to one, can't graphic it")
            sys.exit(1)

    def createLists(self, points, pointsNew, rangePoints, gamesPlayed):
        """Create lists points and range."""
        points = [3.0, 1.0, 0.25, 0.5, 3.0, 0.25, 3.0, 1.0, 2.5, 2, 3.0, 0, 0, 0.75, 3.0, 1.0, 0.25, 0.5,
                  0, 0.25, 3.0, 1.0, 3.0, 0, 0, 0.75, 3.0, 1.0, 0.25, 3.0, 1.0, 0.5, 2.5, 0.5, 0, 0, 0.75, 3.0]
        temp = 0
        for i in range(0, gamesPlayed):
            pointsNew[i] = points[i] - 1.5 + temp
            temp = pointsNew[i]
        for j in range(1, gamesPlayed + 1):
            rangePoints[j - 1] = j

    def createGraphic(self, pointsNew, rangePoints, gamesPlayed):
        """Create graphic."""
        plt.rcParams['toolbar'] = 'None'
        fig, ax = plt.subplots(figsize=(10, 2))
        fig.tight_layout()
        fig.patch.set_facecolor('xkcd:gray')
        ax.scatter(rangePoints, pointsNew, color='b')
        ax.plot(rangePoints, pointsNew, color='k')
        ax.set_xlim(0, gamesPlayed)
        ax.set_facecolor('xkcd:gray')
        ax.set_yticklabels([])
        ax.set_ylabel('Puntuación', fontsize=10)
        ax.set_xlabel('Jornadas', fontsize=10)
        ax.set_title('Club\n')
        ax.grid(linestyle='--', linewidth=0.5)
        # plt.show()

        return fig
