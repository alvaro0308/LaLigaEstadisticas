"""LaLigaEstadisticas App."""

# Filename: LaLigaEstadisticas.py
# export PYTHONIOENCODING=utf-8

from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
from AppUI import AppUI
from openpyxl import load_workbook
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

__version__ = "alpha"
__author__ = "Álvaro"


class App:
    """."""

    def __init__(self):
        """."""
        # workbook = load_workbook(
        #     filename="/home/alvaro/github/LaLigaEstadisticas/Quiniela 21-22 Antigua.xlsx")
        workbook = load_workbook(
            filename="/home/alvaro/github/LaLigaEstadisticas/Quiniela 21-22.xlsx")
        self.sheet = workbook.active

        maxClubsSantander = 20
        maxClubsSmartbank = 22
        firstRowSantander = 3
        firstRowSmartbank = 25
        self.gamesPlayed = 38

        listClubsSantander = []
        listClubsSmartbank = []
        dictCommentsSantander = {}
        dictCommentsSmartbank = {}
        self.readClubs(listClubsSantander, maxClubsSantander,
                       firstRowSantander)
        self.readClubs(listClubsSmartbank, maxClubsSmartbank,
                       firstRowSmartbank)
        for clubSantander in listClubsSantander:
            dictCommentsSantander[clubSantander] = self.readCommentsClubs(listClubsSmartbank, maxClubsSmartbank,
                                                                          firstRowSmartbank, clubSantander)
        for clubSmartbank in listClubsSmartbank:
            dictCommentsSmartbank[clubSmartbank] = self.readCommentsClubs(listClubsSmartbank, maxClubsSmartbank,
                                                                          firstRowSmartbank, clubSmartbank)

        self.app = QApplication(sys.argv)
        self.darkMode()
        view = AppUI(self.sheet, listClubsSantander, listClubsSmartbank, dictCommentsSantander, dictCommentsSmartbank,
                     maxClubsSantander, maxClubsSmartbank, self.gamesPlayed,
                     firstRowSantander, firstRowSmartbank)
        view.show()
        sys.exit(self.app.exec_())

    def readClubs(self, listClubs, maxClubs, firstRow):
        """."""
        for cell in self.sheet.iter_rows(min_row=firstRow,
                                         max_row=maxClubs + firstRow - 1,
                                         min_col=5, max_col=5,
                                         values_only=True):
            listClubs.append(cell[0])
            # print(cell[0])

    def readCommentsClubs(self, listClubs, maxClubs, firstRow, club):
        """."""
        counterBlank = 0
        currentRow = 3
        listComments = []
        for cell in self.sheet.iter_rows(min_row=3,
                                         min_col=2, max_col=2,
                                         values_only=True):
            # listClubs.append(cell[0])
            if cell[0] is None:
                counterBlank += 1
            else:
                counterBlank = 0
            if counterBlank > 2:
                break
            clubs = str(self.sheet.cell(currentRow, 1).value).split(" - ")
            for i in clubs:
                if i == club:
                    # print(clubs)
                    # print(str(self.sheet.cell(currentRow, 1).
                    #           value) + " " + str(cell[0]) + " " + str(self.sheet.cell(currentRow, 3).
                    #                                                   value))
                    listComments.append(str(self.sheet.cell(currentRow, 1).
                                            value) + ": " + str(cell[0]) + "_ " + str(self.sheet.cell(currentRow, 3).
                                                                                      value))
            currentRow += 1

        return listComments

    def darkMode(self):
        """."""
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
    """Is main function."""
    App()


if __name__ == '__main__':
    main()
    # appctxt = ApplicationContext()
    # window = QMainWindow()
    # window.resize(250, 150)
    # window.show()
    # exit_code = appctxt.app.exec_()
