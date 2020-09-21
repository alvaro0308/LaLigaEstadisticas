"""LaLigaEstadisticas App."""

# Filename: AppUI.py

import sys
import sip
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QRadioButton

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
    workbook = load_workbook(filename="Quiniela.xlsx")
    workbook.sheetnames
    sheet = workbook.active

    maxClubsSantander = 20
    maxClubsSmartbank = 22
    firstRowSantander = 3
    firstRowSmartbank = 25
    firstCol = 7
    lastCol = 44

    gamesPlayed = 38

    print("Liga Santander")
    printPoints(sheet, firstRowSantander, firstCol,
                lastCol, maxClubsSantander, gamesPlayed)
    print("\nLiga Smartbank")
    printPoints(sheet, firstRowSmartbank, firstCol,
                lastCol, maxClubsSmartbank, gamesPlayed)


class AppUI(QMainWindow):
    """Este es el docstring de la funcion."""

    def __init__(self):
        """Este es el docstring de la funcion."""
        super().__init__()
        self.setFixedSize(1000, 1000)
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createBox()
        self._connectSignals()
        self._check = True
        self._radioButtonState = False
        self._radioButton2State = False

    def _createBox(self):
        """Este es el docstring de la funcion."""
        self._box = QComboBox()
        self._box.addItems(["Seleccione un campeonato",
                            "Liga Santander", "Liga Smartbank"])
        self.setWindowTitle("LaLigaEstadisticas")
        self.generalLayout.addWidget(self._box)

    def _createRadioButton(self):
        """Este es el docstring de la funcion."""
        self.radioButtons = {}
        radioButtonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        self.radioButtons = {
            "1": (0, 0),
            "2": (0, 1),
            "3": (1, 0),
            "4": (1, 1),
            "5": (2, 0),
            "6": (2, 1),
            "7": (3, 0),
            "8": (3, 1),
            "9": (4, 0),
            "10": (4, 1),
            "11": (5, 0),
            "12": (5, 1),
            "13": (6, 0),
            "14": (6, 1),
            "15": (7, 0),
            "16": (7, 1),
            "17": (8, 0),
            "18": (8, 1),
            "19": (9, 0),
            "20": (9, 1),
        }
        # Create the buttons and add them to the grid layout
        for btnText, pos in self.radioButtons.items():
            self.radioButtons[btnText] = QRadioButton(btnText)
            self.radioButtons[btnText].setFixedSize(120, 20)
            self.radioButtons[btnText].setChecked(False)
            radioButtonsLayout.addWidget(self.radioButtons[btnText],
                                         pos[0], pos[1])
            # self._radioButton.toggled.connect(lambda:
            #                                   self.btnstate(self._radioButton))
        self.generalLayout.addLayout(radioButtonsLayout)
        self._radioButtonState = True

    def _createRadioButton2(self):
        """Este es el docstring de la funcion."""
        self.radioButtons2 = {}
        radioButtons2Layout = QGridLayout()
        # Button text | position on the QGridLayout
        self.radioButtons2 = {
            "a": (0, 0),
            "b": (0, 1),
            "c": (1, 0),
            "d": (1, 1),
            "e": (2, 0),
            "f": (2, 1),
            "g": (3, 0),
            "h": (3, 1),
            "i": (4, 0),
            "j": (4, 1),
            "k": (5, 0),
            "l": (5, 1),
            "m": (6, 0),
            "n": (6, 1),
            "o": (7, 0),
            "p": (7, 1),
            "q": (8, 0),
            "r": (8, 1),
            "s": (9, 0),
            "t": (9, 1),
            "u": (10, 0),
            "v": (10, 1),
        }
        # Create the buttons and add them to the grid layout
        for btnText, pos in self.radioButtons2.items():
            self.radioButtons2[btnText] = QRadioButton(btnText)
            self.radioButtons2[btnText].setFixedSize(120, 20)
            self.radioButtons2[btnText].setChecked(False)
            radioButtons2Layout.addWidget(self.radioButtons2[btnText],
                                          pos[0], pos[1])
            # self._radioButton.toggled.connect(lambda:
            #                                   self.btnstate(self._radioButton))
        self.generalLayout.addLayout(radioButtons2Layout)
        self._radioButton2State = True

    def _clearRadioButtons(self):
        if self._radioButtonState:
            for btnText, pos in self.radioButtons.items():
                sip.delete(self.radioButtons[btnText])
            self._radioButtonState = False
        if self._radioButton2State:
            for btnText, pos in self.radioButtons2.items():
                sip.delete(self.radioButtons2[btnText])
            self._radioButton2State = False

    def _connectSignals(self):
        """Este es el docstring de la funcion."""
        self._box.currentIndexChanged.connect(self._printBox)

    def _printBox(self):
        """Este es el docstring de la funcion."""
        if self._box.currentText() == "Seleccione un campeonato":
            self._clearRadioButtons()
        else:
            print("Campeonato seleccionado: ", self._box.currentText())
            if self._check:
                # self._check = False
                if self._box.currentText() == "Liga Santander":
                    self._clearRadioButtons()
                    self._createRadioButton()
                elif self._box.currentText() == "Liga Smartbank":
                    self._clearRadioButtons()
                    self._createRadioButton2()


def main2():
    """Second main funtion."""
    # Create an instance of `QApplication`
    LaLiga = QApplication(sys.argv)
    # Show the calculator's GUI
    view = AppUI()
    view.show()
    # Create instances of the model and the controller
    # model = evaluateExpression
    # AppCtrl(view = view)
    # Execute calculator's main loop
    sys.exit(LaLiga.exec_())


if __name__ == '__main__':
    main2()
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = QMainWindow()
    window.resize(250, 150)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
