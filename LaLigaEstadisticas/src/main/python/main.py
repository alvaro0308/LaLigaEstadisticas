"""LaLigaEstadisticas App."""

# Filename: AppUI.py
# export PYTHONIOENCODING=utf-8

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from AppUI import AppUI
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

__version__ = "alpha"
__author__ = "Álvaro"

ERROR_MSG = "ERROR"


def printPoints(sheet, firstRow, firstCol, lastCol, maxClubs, gamesPlayed):
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

            print(points)
            checkGames(gamesPlayed)
            createLists(points, pointsNew, rangePoints, gamesPlayed)
            createGraphic(pointsNew, rangePoints, gamesPlayed)


def checkGames(gamesPlayed):
    """Check number of games."""
    if gamesPlayed == 1:
        print("Games played is equal to one, can't graphic it")
        sys.exit(1)


def createLists(points, pointsNew, rangePoints, gamesPlayed):
    """Create lists points and range."""
    temp = 0
    for i in range(0, gamesPlayed):
        pointsNew[i] = points[i] - 1.5 + temp
        temp = pointsNew[i]
    for j in range(1, gamesPlayed + 1):
        rangePoints[j - 1] = j


def readClubs(listClubs, maxClubs, firstRow, sheet):
    """."""
    for cell in sheet.iter_rows(min_row=firstRow,
                                max_row=maxClubs + firstRow - 1,
                                min_col=5, max_col=5,
                                values_only=True):
        listClubs.append(cell[0])


def createGraphic(pointsNew, rangePoints, gamesPlayed):
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
    plt.show()


def main():
    """Is main function."""
    workbook = load_workbook(
        filename="/home/alvaro/github/LaLigaEstadisticas/Quiniela.xlsx")
    sheet = workbook.active

    maxClubsSantander = 20
    maxClubsSmartbank = 22
    firstRowSantander = 3
    firstRowSmartbank = 25
    firstCol = 7
    lastCol = 44

    gamesPlayed = 38

    listClubsSantander = []
    listClubsSmartbank = []
    readClubs(listClubsSantander, maxClubsSantander,
              firstRowSantander, sheet)
    readClubs(listClubsSmartbank, maxClubsSmartbank,
              firstRowSmartbank, sheet)

    # print("Liga Santander")
    # printPoints(sheet, firstRowSantander, firstCol,
    #             lastCol, maxClubsSantander, gamesPlayed)
    # print("\nLiga Smartbank")
    # printPoints(sheet, firstRowSmartbank, firstCol,
    #             lastCol, maxClubsSmartbank, gamesPlayed)

    app = QApplication(sys.argv)
    view = AppUI(listClubsSantander, listClubsSmartbank)
    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = QMainWindow()
    window.resize(250, 150)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
