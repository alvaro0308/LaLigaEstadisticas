"""AppUI.py."""

from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QToolBar
from PyQt5 import QtCore
import sip

from GraphicExcel import GraphicExcel


class AppUI(QMainWindow):
    """Este es el docstring de la funcion."""

    def __init__(self, sheet, listClubsSantander, listClubsSmartbank):
        """Este es el docstring de la funcion."""
        super().__init__()
        self.listSantander = listClubsSantander
        self.listSmartbank = listClubsSmartbank
        self.setFixedSize(1000, 1000)
        self.layout = QVBoxLayout()

        _centralWidget = QWidget()
        _centralWidget.setLayout(self.layout)
        self.setCentralWidget(_centralWidget)

        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)
        self.currencyList = QComboBox()

        sc = GraphicExcel(sheet)
        #sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.layout.addWidget(sc)

        self._createBox()
        self._connectSignals()
        self._check = True
        self._radioButtonState = False
        self._radioButton2State = False

    def _createBox(self):
        """Este es el docstring de la funcion."""
        self._box = QComboBox()
        self._box.InsertAtTop
        self._box.addItems(["Seleccione un campeonato",
                            "Liga Santander", "Liga Smartbank"])
        self.setWindowTitle("LaLigaEstadisticas")
        self.layout.addWidget(self._box)

    def _createRadioButton(self):
        """Este es el docstring de la funcion."""
        self.radioButtons = {}
        radioButtonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        self.radioButtons = {
            self.listSantander[0]: (0, 0),
            self.listSantander[1]: (1, 0),
            self.listSantander[2]: (2, 0),
            self.listSantander[3]: (3, 0),
            self.listSantander[4]: (4, 0),
            self.listSantander[5]: (5, 0),
            self.listSantander[6]: (6, 0),
            self.listSantander[7]: (7, 0),
            self.listSantander[8]: (8, 0),
            self.listSantander[9]: (9, 0),
            self.listSantander[10]: (0, 1),
            self.listSantander[11]: (1, 1),
            self.listSantander[12]: (2, 1),
            self.listSantander[13]: (3, 1),
            self.listSantander[14]: (4, 1),
            self.listSantander[15]: (5, 1),
            self.listSantander[16]: (6, 1),
            self.listSantander[17]: (7, 1),
            self.listSantander[18]: (8, 1),
            self.listSantander[19]: (9, 1),
        }
        # Create the buttons and add them to the grid layout
        for btnText, pos in self.radioButtons.items():
            self.radioButtons[btnText] = QRadioButton(btnText)
            self.radioButtons[btnText].setFixedSize(140, 90)
            self.radioButtons[btnText].setChecked(False)
            radioButtonsLayout.addWidget(self.radioButtons[btnText],
                                         pos[0], pos[1])
            # self._radioButton.toggled.connect(lambda:
            #                                   self.btnstate(self._radioButton))
        self.layout.addLayout(radioButtonsLayout)
        self._radioButtonState = True

    def _createRadioButton2(self):
        """Este es el docstring de la funcion."""
        self.radioButtons2 = {}
        radioButtons2Layout = QGridLayout()
        # Button text | position on the QGridLayout
        self.radioButtons2 = {
            self.listSmartbank[0]: (0, 0),
            self.listSmartbank[1]: (1, 0),
            self.listSmartbank[2]: (2, 0),
            self.listSmartbank[3]: (3, 0),
            self.listSmartbank[4]: (4, 0),
            self.listSmartbank[5]: (5, 0),
            self.listSmartbank[6]: (6, 0),
            self.listSmartbank[7]: (7, 0),
            self.listSmartbank[8]: (8, 0),
            self.listSmartbank[9]: (9, 0),
            self.listSmartbank[10]: (0, 1),
            self.listSmartbank[11]: (1, 1),
            self.listSmartbank[12]: (2, 1),
            self.listSmartbank[13]: (3, 1),
            self.listSmartbank[14]: (4, 1),
            self.listSmartbank[15]: (5, 1),
            self.listSmartbank[16]: (6, 1),
            self.listSmartbank[17]: (7, 1),
            self.listSmartbank[18]: (8, 1),
            self.listSmartbank[19]: (9, 1),
        }
        # Create the buttons and add them to the grid layout
        for btnText, pos in self.radioButtons2.items():
            self.radioButtons2[btnText] = QRadioButton(btnText)
            self.radioButtons2[btnText].setFixedSize(140, 90)
            self.radioButtons2[btnText].setChecked(False)
            radioButtons2Layout.addWidget(self.radioButtons2[btnText],
                                          pos[0], pos[1])
            # self._radioButton.toggled.connect(lambda:
            #                                   self.btnstate(self._radioButton))
        self.layout.addLayout(radioButtons2Layout)
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
