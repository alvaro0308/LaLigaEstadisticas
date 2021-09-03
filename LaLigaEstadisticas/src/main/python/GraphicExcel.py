"""GraphicExcel.py."""

import sys
from matplotlib.collections import PolyCollection
import mplcursors
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class GraphicExcel(FigureCanvasQTAgg):
    """Este es el docstring de la funcion."""

    def __init__(self, sheet, club, maxClubs, firstRow, listComments, league):
        """Este es el docstring de la funcion."""
        self.firstRow = firstRow
        self.firstCol = 7
        # self.maxGames = 42
        self.APLZ = -10
        self.initPoints = 100
        self.sheet = sheet
        self.club = club
        self.maxClubs = maxClubs
        self.league = league
        if self.league == "Santander":
            self.maxXAxis = 39
            self.maxGames = 38
            self.lastCol = 46
        elif self.league == "Smartbank":
            self.maxXAxis = 43
            self.maxGames = 42
            self.lastCol = 48
        self.listComments = listComments
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
        pointsNew = [None] * self.maxGames
        rangePoints = [None] * self.maxGames
        self.checkGames()
        rowClub = self.getRowClub()

        for value in self.sheet.iter_rows(min_row=rowClub, max_row=rowClub,
                                          min_col=self.firstCol,
                                          max_col=self.lastCol,
                                          values_only=True):
            if self.maxGames == 1:
                points = value[0]
            else:
                points = value[0:self.maxGames]

        self.createLists(points, pointsNew, rangePoints)
        fig = self.createGraphic(pointsNew, rangePoints)

        return fig

    def checkGames(self):
        """Check number of games."""
        if self.maxGames == 1:
            print("Games played is equal to one, can't graphic it")
            sys.exit(1)

    def createLists(self, points, pointsNew, rangePoints):
        """Create lists points and range."""
        temp = 100
        for i in range(0, self.maxGames):
            if points[i] == "APLZ":
                pointsNew[i] = self.APLZ
                pointsNew[i] = None
                continue
            if points[i] == '-' or points[i] is None or (type(points[i]) is not float and type(points[i]) is not int):
                break
            pointsNew[i] = points[i] - 1.5 + temp
            temp = pointsNew[i]
        for j in range(1, self.maxGames + 1):
            rangePoints[j - 1] = j

    def createGraphic(self, pointsNew, rangePoints):
        """Create graphic."""
        plt.rcParams['toolbar'] = 'None'
        fig, ax = plt.subplots(figsize=(10, 2))
        fig.tight_layout()
        fig.patch.set_facecolor('xkcd:gray')
        rangePoints.insert(0, 0)
        pointsNew.insert(0, self.initPoints)
        ax.scatter(rangePoints, pointsNew, color='b')
        lines = ax.plot(rangePoints, pointsNew, color='k')
        # for i in range(0, len(pointsNew)):
        #     if pointsNew[i] == None and pointsNew[i - 1] != None and pointsNew[i + 1] != None:
        #         print("APLZ2 " + str(rangePoints[i]
        #                              ) + " " + str(pointsNew[i - 1]) + " " + str(i))
        #         pointsNew[i] = pointsNew[i - 1]
        #         ax.plot([i - 1, i], [pointsNew[i - 1], pointsNew[i - 1]], linestyle='--',
        #                 linewidth=0.5, color='r')
        #         ax.plot([i, i + 1], [pointsNew[i], pointsNew[i + 1]], color='k')
        #         ax.scatter(rangePoints[i], pointsNew[i-1], color='r')
        prevElem = self.initPoints
        postElem = None
        print(pointsNew)
        for i in range(0, len(pointsNew)):
            if pointsNew[i] == None:
                aux = i
                aux2 = i
                while aux >= 0:
                    if pointsNew[aux] != None:
                        prevElem = aux
                        break
                    aux -= 1
                while aux2 < len(pointsNew):
                    if pointsNew[aux2] != None:
                        postElem = aux2
                        break
                    aux2 += 1
                print(
                    "APLZ2 " + str(rangePoints[i]) + " " + str(pointsNew[prevElem]) + " " + str(i))
                pointsNew[i] = pointsNew[prevElem]
                ax.plot([prevElem, i], [pointsNew[prevElem], pointsNew[prevElem]], linestyle='--',
                        linewidth=0.5, color='r')
                if pointsNew[i + 1] != None:
                    ax.plot([i, postElem], [pointsNew[i],
                                            pointsNew[postElem]], color='k')
                ax.scatter(rangePoints[i], pointsNew[prevElem], color='r')

        ax.set_xlim(0, self.maxXAxis)
        ax.set_ylim([self.initPoints - 10, self.initPoints + 10])
        ax.set_facecolor('xkcd:gray')
        ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.set_ylabel('Puntuación', fontsize=12)
        ax.set_xlabel('Jornadas', fontsize=12)
        ax.set_title(self.club, fontsize=12)
        ax.grid(linestyle='--', linewidth=0.5)

        def onAdd(sel):
            if int(sel.target[0]) == 0:
                text = "Inicio"
            elif int(sel.target[0]) - 1 > len(self.listComments) - 1:
                text = ""
            else:
                text = self.listComments[int(
                    sel.target[0]) - 1].replace("_ ", "\n")
            sel.annotation.set_text(text)
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
            lines, ax=ax, func=onAdd, hover=False)
        plt.close(fig)

        return fig
