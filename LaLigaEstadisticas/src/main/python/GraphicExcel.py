"""GraphicExcel.py."""

import sys
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
        gamesDelayed = []
        gamesDelayedAndPlayed = []
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

        points = list(points)

        for i in range(0, len(points)):
            if points[i] != '-' and not points[i].isupper():
                points[i] = float(points[i].replace(",", "."))

        points = self.detectDelayedAndPlayed(
            points, gamesDelayed, gamesDelayedAndPlayed)
        pointsNew = self.createLists(
            points, pointsNew, rangePoints, gamesDelayed)

        fig = self.createGraphic(
            pointsNew, rangePoints, gamesDelayed, gamesDelayedAndPlayed)

        return fig

    def checkGames(self):
        """Check number of games."""
        if self.maxGames == 1:
            print("Games played is equal to one, can't graphic it")
            sys.exit(1)

    def detectDelayedAndPlayed(self, points, gamesDelayed, gamesDelayedAndPlayed):
        for i in range(0, len(points)):
            if type(points[i]) is str and "APLZ J" in points[i]:
                splitted = points[i].split(" ")
                if "J" in splitted[1]:
                    roundDelayed = int(splitted[1].replace('J', ''))
                if "," in splitted[2]:
                    pointsDelayed = splitted[2].replace(',', '.')
                else:
                    pointsDelayed = splitted[2]

                try:
                    pointsDelayed = float(pointsDelayed)
                    points[i] = self.APLZ
                    gamesDelayed.append(i + 1)
                    gamesDelayedAndPlayed.append(roundDelayed)
                    points.insert(roundDelayed - 1, pointsDelayed)
                except ValueError:
                    print("Error casting points to float")

        return [i for i in points if i != self.APLZ]

    def createLists(self, points, pointsNew, rangePoints, gamesDelayed):
        """Create lists points and range."""
        temp = 100
        for i in range(0, self.maxGames):
            if points[i] == "APLZ":
                pointsNew[i] = None
                gamesDelayed.append(i)
                continue
            if points[i] == '-' or points[i] is None or (type(points[i]) is not float and type(points[i]) is not int):
                break
            pointsNew[i] = points[i] - 1.5 + temp
            temp = pointsNew[i]
        for j in range(1, self.maxGames + 1):
            rangePoints[j - 1] = j

        return pointsNew

    def createGraphic(self, pointsNew, rangePoints, gamesDelayed, gamesDelayedAndPlayed):
        """Create graphic."""
        plt.rcParams['toolbar'] = 'None'
        fig, ax = plt.subplots(figsize=(10, 2))
        fig.tight_layout()
        fig.patch.set_facecolor('xkcd:gray')
        rangePoints.insert(0, 0)
        pointsNew.insert(0, self.initPoints)
        ax.scatter(rangePoints, pointsNew, color='b')
        linesCursor = ax.plot(rangePoints, pointsNew, color='k')
        prevElem = self.initPoints
        postElem = None

        for i in range(0, len(pointsNew) - 1):
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
                pointsNew[i] = pointsNew[prevElem]
                linesCursor += ax.plot([prevElem, i], [pointsNew[prevElem], pointsNew[prevElem]], linestyle='--',
                                       linewidth=0.5, color='r')
                if pointsNew[i + 1] != None:
                    ax.plot([i, postElem], [pointsNew[i],
                                            pointsNew[postElem]], color='k')
                ax.scatter(rangePoints[i], pointsNew[prevElem], color='r')

        for j in range(0, len(gamesDelayed)):
            ax.scatter(gamesDelayed[j],
                       pointsNew[gamesDelayed[j]], color='r')

        for l in range(0, len(gamesDelayedAndPlayed)):
            ax.scatter(gamesDelayedAndPlayed[l],
                       pointsNew[gamesDelayedAndPlayed[l]], color='g')
            ax.plot(
                [gamesDelayedAndPlayed[l] - 1, gamesDelayedAndPlayed[l]], [pointsNew[gamesDelayedAndPlayed[l] - 1], pointsNew[gamesDelayedAndPlayed[l]]], color='g')

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

        def mplcursorPoints(linesCursor, ax=None, func=None, **kwargs):
            scats = [ax.scatter(x=line.get_xdata(), y=line.get_ydata(),
                                color='none') for line in linesCursor]
            cursor = mplcursors.cursor(scats, **kwargs)
            if func is not None:
                cursor.connect('add', func)
            return cursor

        mplcursorPoints(
            linesCursor, ax=ax, func=onAdd, hover=False)
        plt.close(fig)

        return fig
