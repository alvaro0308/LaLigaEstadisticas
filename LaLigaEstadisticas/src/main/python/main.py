"""LaLigaEstadisticas App."""

# Filename: LaLigaEstadisticas.py
# export PYTHONIOENCODING=utf-8

# from fbs_runtime.application_context.PyQt5 import ApplicationContext
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
        workbook = load_workbook(
            filename="/home/alvaro/github/LaLigaEstadisticas/Quiniela.xlsx")
        self.sheet = workbook.active

        maxClubsSantander = 20
        maxClubsSmartbank = 22
        firstRowSantander = 3
        firstRowSmartbank = 25
        self.gamesPlayed = 38

        listClubsSantander = []
        listClubsSmartbank = []
        self.readClubs(listClubsSantander, maxClubsSantander,
                       firstRowSantander)
        self.readClubs(listClubsSmartbank, maxClubsSmartbank,
                       firstRowSmartbank)

        self.app = QApplication(sys.argv)
        self.darkMode()
        view = AppUI(self.sheet, listClubsSantander, listClubsSmartbank,
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
