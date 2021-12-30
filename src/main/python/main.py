"""LaLigaEstadisticas App"""

# export PYTHONIOENCODING=utf-8

import sys
import yaml
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from AppUI import AppUI
from ConfigApp import ConfigApp
from PyQt5.QtCore import Qt
from openpyxl import load_workbook
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication


__version__ = "alpha"
__author__ = "Alvaro"


class App:
    """LaLigaEstadisticas App"""

    def __init__(self, path):
        """Read clubs and launch Application"""
        with open(path) as f:
            self.params = yaml.load(f, Loader=yaml.FullLoader)
        path = path.replace("config/config.yaml", "")
        self.params['path'] = path

        workbook = load_workbook(
            filename=self.params['path'] + self.params['databasePath']
            + self.params['nameDownloadedDatabase'] + self.params['extensionDatabase'])
        self.sheet = workbook.active

        self.firstCol = self.params['firstColPoints']
        self.APLZ = -10

        maxClubsSantander = self.params['maxClubsSantander']
        maxClubsSmartbank = self.params['maxClubsSmartbank']
        firstRowSantander = self.params['firstRowSantander']
        firstRowSmartbank = self.params['firstRowSmartbank']

        maxGamesSantander = self.params['maxGamesSantander']
        lastColSantander = self.params['lastColPointsSantander']
        maxGamesSmartbank = self.params['maxGamesSmartbank']
        lastColSmartbank = self.params['lastColPointsSmartbank']

        listClubsSantander = []
        listClubsSmartbank = []
        dictMistersSantander = {}
        dictMistersSmartbank = {}
        dictCommentsSantander = {}
        dictCommentsSmartbank = {}
        dictPointsSantander = {}
        dictPointsSmartbank = {}
        dictRangePointsSantander = {}
        dictRangePointsSmartbank = {}
        dictGamesDelayedSantander = {}
        dictGamesDelayedSmartbank = {}
        dictGamesDelayedAndPlayedSantander = {}
        dictGamesDelayedAndPlayedSmartbank = {}
        dictGamesAheadSantander = {}
        dictGamesAheadSmartbank = {}

        self.readClubs(listClubsSantander, maxClubsSantander,
                       firstRowSantander)
        self.readClubs(listClubsSmartbank, maxClubsSmartbank,
                       firstRowSmartbank)

        self.readMisters(dictMistersSantander, maxClubsSantander,
                         firstRowSantander)
        self.readMisters(dictMistersSmartbank, maxClubsSmartbank,
                         firstRowSmartbank)

        for clubSantander in listClubsSantander:
            dictCommentsSantander[clubSantander] = self.readCommentsClubs(
                clubSantander)
        for clubSmartbank in listClubsSmartbank:
            dictCommentsSmartbank[clubSmartbank] = self.readCommentsClubs(
                clubSmartbank)

        self.readAllPointsClubs(
            listClubsSantander, maxGamesSantander, firstRowSantander,
            maxClubsSantander, lastColSantander, dictCommentsSantander,
            dictPointsSantander, dictRangePointsSantander, dictGamesDelayedSantander,
            dictGamesDelayedAndPlayedSantander, dictGamesAheadSantander)

        self.readAllPointsClubs(
            listClubsSmartbank, maxGamesSmartbank, firstRowSmartbank,
            maxClubsSmartbank, lastColSmartbank, dictCommentsSmartbank,
            dictPointsSmartbank, dictRangePointsSmartbank, dictGamesDelayedSmartbank,
            dictGamesDelayedAndPlayedSmartbank, dictGamesAheadSmartbank)

        dictStandingSantander = self.standing(
            listClubsSantander, dictPointsSantander)
        dictStandingSmartbank = self.standing(
            listClubsSmartbank, dictPointsSmartbank)

        dictStandingSantander = dict(
            sorted(dictStandingSantander.items(), key=lambda item: item[1], reverse=True))
        dictStandingSmartbank = dict(
            sorted(dictStandingSmartbank.items(), key=lambda item: item[1], reverse=True))

        self.app = QApplication(sys.argv)
        self.darkMode()
        view = AppUI(self.sheet, listClubsSantander, listClubsSmartbank,
                     dictMistersSantander, dictMistersSmartbank,
                     dictCommentsSantander, dictCommentsSmartbank,
                     maxClubsSantander, maxClubsSmartbank,
                     firstRowSantander, firstRowSmartbank, dictPointsSantander,
                     dictPointsSmartbank, dictRangePointsSantander, dictRangePointsSmartbank,
                     dictGamesDelayedSantander, dictGamesDelayedSmartbank, dictGamesDelayedAndPlayedSantander,
                     dictGamesDelayedAndPlayedSmartbank, dictGamesAheadSantander, dictGamesAheadSmartbank,
                     dictStandingSantander, dictStandingSmartbank, self.params)
        view.show()
        sys.exit(self.app.exec_())

    def standing(self, listClubs, dictPoints):
        dictStanding = {}
        for club in listClubs:
            for i in range(len(dictPoints[club]) - 1, 0, -1):
                if dictPoints[club][i] != None:
                    dictStanding[club] = dictPoints[club][i]
                    break

        return dictStanding

    def readClubs(self, listClubs, maxClubs, firstRow):
        """Read clubs from database"""
        for cell in self.sheet.iter_rows(min_row=firstRow,
                                         max_row=maxClubs + firstRow - 1,
                                         min_col=5, max_col=5,
                                         values_only=True):
            listClubs.append(cell[0])

    def readMisters(self, dictMisters, maxClubs, firstRow):
        """Read misters from database"""
        listNamesMister = []
        for cell in self.sheet.iter_rows(min_row=firstRow,
                                         max_row=maxClubs + firstRow - 1,
                                         min_col=5, max_col=5,
                                         values_only=True):
            listNamesMister.append(cell[0])

        currentMister = 0
        for cell in self.sheet.iter_rows(min_row=firstRow,
                                         max_row=maxClubs + firstRow - 1,
                                         min_col=6, max_col=6,
                                         values_only=True):
            dictMisters[listNamesMister[currentMister]] = cell[0]
            currentMister += 1

    def readCommentsClubs(self, club):
        """Read comments clubs from database"""
        counterBlank = 0
        currentRow = 3
        listComments = []
        for cell in self.sheet.iter_rows(min_row=3,
                                         min_col=2, max_col=2,
                                         values_only=True):

            if cell[0] is None:
                counterBlank += 1
            else:
                counterBlank = 0
            # if counterBlank > 2:
            #     break
            clubs = str(self.sheet.cell(currentRow, 1).value).split(" - ")
            for i in clubs:
                if i == club:
                    listComments.append(str(self.sheet.cell(currentRow, 1).value) + ": "
                                        + str(cell[0]) + "_ "
                                        + str(self.sheet.cell(currentRow, 3).value))
            currentRow += 1

        return listComments

    def checkGames(self, maxGames):
        """Check number of games"""
        if maxGames == 1:
            print("Games played is equal to one, can't graphic it")
            sys.exit(1)

    def getRowClub(self, firstRow, maxClubs, club):
        """Get row club from Excel database"""
        rowClub = firstRow
        for value in self.sheet.iter_rows(min_row=firstRow,
                                          max_row=firstRow
                                          + maxClubs - 1,
                                          min_col=5,
                                          max_col=5,
                                          values_only=True):
            if club == value[0]:
                return rowClub
            rowClub += 1

        return -1

    def createLists(self, points, pointsNew, rangePoints, gamesDelayed, maxGames):
        """Create lists points and range"""
        temp = 100
        for i in range(0, maxGames):
            if points[i] == self.params['formatDelayed']:
                pointsNew[i] = None
                gamesDelayed.append(i)
                continue
            if points[i] == '-' or points[i] is None or (type(points[i]) is not float and type(points[i]) is not int):
                break
            pointsNew[i] = points[i] - 1.5 + temp
            temp = pointsNew[i]
        for j in range(1, maxGames + 1):
            rangePoints[j - 1] = j

        return pointsNew

    def detectDelayedAndPlayed(self, points, gamesDelayedAndPlayed, gamesAhead, listComments):
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

                    listComments.insert(
                        roundDelayed - 1, listComments[i])
                    listComments[i] = self.APLZ
                    gamesDelayedAndPlayed.append(roundDelayed - 1)
                    points.insert(roundDelayed - 1, pointsDelayed)
                except ValueError:
                    print("Error casting points to float")
            elif type(points[i]) is str and self.params['formatAhead'] in points[i]:
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

                    listComments.insert(
                        roundDelayed, listComments[i])
                    listComments[i + 1] = self.APLZ
                    gamesAhead.append(roundDelayed)
                    points.insert(roundDelayed, pointsDelayed)
                except ValueError:
                    print("Error casting points to float")
        return [i for i in points if i != self.APLZ], [i for i in listComments if i != self.APLZ]

    def readAllPointsClubs(self, listClubs, maxGames, firstRow, maxClubs, lastCol, dictComments, dictPoints, dictRangePoints, dictGamesDelayed, dictGamesDelayedAndPlayed, dictGamesAhead):
        """Print points clubs"""
        self.checkGames(maxGames)

        for club in listClubs:
            pointsNew = [None] * maxGames
            rangePoints = [None] * maxGames
            gamesDelayed = []
            gamesDelayedAndPlayed = []
            gamesAhead = []
            rowClub = self.getRowClub(firstRow, maxClubs, club)

            for value in self.sheet.iter_rows(min_row=rowClub, max_row=rowClub,
                                              min_col=self.firstCol,
                                              max_col=lastCol,
                                              values_only=True):
                if maxGames == 1:
                    points = value[0]
                else:
                    points = value[0:maxGames]

            points = list(points)

            for i in range(0, len(points)):
                if type(points[i]) is str and points[i] != '-' and not points[i].isupper():
                    try:
                        points[i] = float(points[i].replace(",", "."))
                    except ValueError:
                        print("Error casting points to float")

            points, dictComments[club] = self.detectDelayedAndPlayed(
                points, gamesDelayedAndPlayed, gamesAhead, dictComments[club])
            pointsNew = self.createLists(
                points, pointsNew, rangePoints, gamesDelayed, maxGames)
            dictPoints[club] = pointsNew
            dictRangePoints[club] = rangePoints
            dictGamesDelayed[club] = gamesDelayed
            dictGamesDelayedAndPlayed[club] = gamesDelayedAndPlayed
            dictGamesAhead[club] = gamesAhead

    def darkMode(self):
        """Apply dark mode to Application"""
        self.app.setStyle('Fusion')
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(15, 15, 15))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(0, 87, 184).lighter())
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.app.setPalette(palette)


def main():
    """Is main function"""
    configApp = ConfigApp()
    App(configApp.path)


if __name__ == '__main__':
    main()
