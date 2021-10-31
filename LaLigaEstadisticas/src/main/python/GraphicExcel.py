"""GraphicExcel.py"""

import sys
import mplcursors
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class GraphicExcel(FigureCanvasQTAgg):
    """Create graphic getting data from Excel database"""

    def __init__(self, sheet, club, maxClubs, firstRow, listMisters, listComments, params, league):
        """Create figure"""
        self.params = params
        self.firstRow = firstRow
        self.firstCol = self.params['firstColPoints']
        self.APLZ = -10
        self.initPoints = self.params['initPoints']
        self.sheet = sheet
        self.club = club
        self.maxClubs = maxClubs
        self.league = league
        if self.league == "Santander":
            self.maxGames = self.params['maxGamesSantander']
            self.maxXAxis = self.maxGames + 1
            self.lastCol = self.params['lastColPointsSantander']
        elif self.league == "Smartbank":
            self.maxGames = self.params['maxGamesSmartbank']
            self.maxXAxis = self.maxGames + 1
            self.lastCol = self.params['lastColPointsSmartbank']

        self.listMisters = listMisters.split()
        for i in range(0, len(self.listMisters)):
            self.listMisters[i] = self.listMisters[i].replace(":", "")
            self.listMisters[i] = self.listMisters[i].replace(",", "")
        self.getPathsMisters()
        self.listComments = listComments

        fig = self.printPointsClub()
        super(GraphicExcel, self).__init__(fig)

    def getPathsMisters(self):
        path = str(self.params['path']) + \
            str(self.params['resourcesPath'] +
                str(self.params['mistersPath']) + str(self.club))
        for i in range(0, len(self.listMisters), 2):
            self.listMisters[i + 1] = path + str(self.listMisters[i + 1]) + \
                str(self.params['extensionImage'])

    def getRowClub(self):
        """Get row club from Excel database"""
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
        """Print points clubs"""
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
            if type(points[i]) is str and points[i] != '-' and not points[i].isupper():
                try:
                    points[i] = float(points[i].replace(",", "."))
                except ValueError:
                    print("Error casting points to float")

        points = self.detectDelayedAndPlayed(
            points, gamesDelayed, gamesDelayedAndPlayed)
        pointsNew = self.createLists(
            points, pointsNew, rangePoints, gamesDelayed)

        fig = self.createGraphic(
            pointsNew, rangePoints, gamesDelayed, gamesDelayedAndPlayed)

        return fig

    def checkGames(self):
        """Check number of games"""
        if self.maxGames == 1:
            print("Games played is equal to one, can't graphic it")
            sys.exit(1)

    def detectDelayedAndPlayed(self, points, gamesDelayed, gamesDelayedAndPlayed):
        """Detect delayed and played games"""
        for i in range(0, len(points)):
            if type(points[i]) is str and self.params['formatDelayedAndPlayed'] in points[i]:
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
        """Create lists points and range"""
        temp = 100
        for i in range(0, self.maxGames):
            if points[i] == self.params['formatDelayed']:
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

    def deleteNotPlayed(self, pointsNew):
        """Delete not played games"""
        lastElement = 0
        for i in range(0, len(pointsNew)):
            if pointsNew[i] != None:
                lastElement = i

        del pointsNew[lastElement + 1:len(pointsNew)]

    def createGraphic(self, pointsNew, rangePoints, gamesDelayed, gamesDelayedAndPlayed):
        """Create graphic"""
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
        self.deleteNotPlayed(pointsNew)

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
                [gamesDelayedAndPlayed[l] - 1, gamesDelayedAndPlayed[l]],
                [pointsNew[gamesDelayedAndPlayed[l] - 1], pointsNew[gamesDelayedAndPlayed[l]]], color='g')

        ax.set_xlim(0, self.maxXAxis)
        ax.set_ylim([self.initPoints - 10, self.initPoints + 10])
        ax.set_facecolor('xkcd:gray')
        ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.set_ylabel('Puntuación', fontsize=12)
        ax.set_xlabel('Jornadas', fontsize=12)
        ax.set_title(self.club, fontsize=12)
        ax.grid(linestyle='--', linewidth=0.5)

        for i in range(0, len(self.listMisters), 2):
            if "!!" in self.listMisters[i + 1]:
                zoom = self.params['highZoom']
                self.listMisters[i + 1] = self.listMisters[i +
                                                           1].replace("!!", "")
            elif "!" in self.listMisters[i + 1]:
                zoom = self.params['mediumZoom']
                self.listMisters[i + 1] = self.listMisters[i +
                                                           1].replace("!", "")
            elif "¡" in self.listMisters[i + 1]:
                zoom = self.params['verySmallZoom']
                self.listMisters[i + 1] = self.listMisters[i +
                                                           1].replace("¡", "")
            else:
                zoom = self.params['smallZoom']

            imageMister = mpimg.imread(self.listMisters[i + 1])
            imagebox = OffsetImage(imageMister, zoom=zoom)

            if int(self.listMisters[i]) == 1:
                start = self.params['misterPosStart']
            else:
                start = 0
                ax.arrow(int(self.listMisters[i]) + start, self.params['misterPosHeight'],
                         self.params['arrowX'], self.params['arrowY'], head_width=self.params['arrowHeadWidth'],
                         head_length=self.params['arrowHeadLength'], fc='k', ec='k')
                start = -self.params['misterIncrement']
            ab = AnnotationBbox(
                imagebox, (int(self.listMisters[i]) + start + self.params['misterIncrement'],
                           self.params['misterPosHeight']), frameon=False)

            ax.add_artist(ab)

        def onAdd(sel):
            """Cursor function"""
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
            """Cursor points"""
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
