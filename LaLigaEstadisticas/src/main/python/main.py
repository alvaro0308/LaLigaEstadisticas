"""LaLigaEstadisticas App."""

# Filename: AppUI.py
# export PYTHONIOENCODING=utf-8

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from AppUI import AppUI
from openpyxl import load_workbook
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

__version__ = "alpha"
__author__ = "Álvaro"

ERROR_MSG = "ERROR"


def readClubs(listClubs, maxClubs, firstRow, sheet):
    """."""
    for cell in sheet.iter_rows(min_row=firstRow,
                                max_row=maxClubs + firstRow - 1,
                                min_col=5, max_col=5,
                                values_only=True):
        listClubs.append(cell[0])


def darkMode(app):
    """."""
    app.setStyle('Fusion')
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
    app.setPalette(palette)


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
    darkMode(app)
    view = AppUI(sheet, listClubsSantander, listClubsSmartbank)
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
