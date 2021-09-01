"""AppUI.py."""

import sip
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QMainWindow
from functools import partial
from GraphicExcel import GraphicExcel
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap


class AppUI(QMainWindow):
    """Este es el docstring de la funcion."""

    def __init__(self, sheet, listClubsSantander, listClubsSmartbank,
                 dictCommentsSantander, dictCommentsSmartbank,
                 maxClubsSantander, maxClubsSmartbank, gamesPlayed,
                 firstRowSantander, firstRowSmartbank):
        """Este es el docstring de la funcion."""
        super().__init__()
        self.listSantander = listClubsSantander
        self.listSantanderDuplicated = listClubsSantander.copy()
        for i in range(0, len(self.listSantanderDuplicated)):
            self.listSantanderDuplicated[i] += "2"
        self.listSmartbank = listClubsSmartbank
        self.listSmartbankDuplicated = listClubsSmartbank.copy()
        for i in range(0, len(self.listSmartbankDuplicated)):
            self.listSmartbankDuplicated[i] += "2"
        self.dictCommentsSantander = dictCommentsSantander
        self.dictCommentsSmartbank = dictCommentsSmartbank
        self.maxClubsSantander = maxClubsSantander
        self.maxClubsSmartbank = maxClubsSmartbank
        self.firstRowSantander = firstRowSantander
        self.firstRowSmartbank = firstRowSmartbank
        self.showMaximized()
        self.layout = QGridLayout()
        self.sheet = sheet

        _centralWidget = QWidget()
        _centralWidget.setLayout(self.layout)
        self.setCentralWidget(_centralWidget)

        self._createBox()
        self._connectSignals()
        # self._check = True
        self._radioButtonState = False
        self._radioButton2State = False

    def _createBox(self):
        """Este es el docstring de la funcion."""
        self._box = QComboBox()
        self._box.InsertAtTop
        self._box.addItems(["Seleccione un campeonato",
                            "Liga Santander", "Liga Smartbank"])
        self.setWindowTitle("LaLigaEstadisticas")
        self.layout.addWidget(self._box, 0, 0)

    def _createRadioButton(self):
        """Este es el docstring de la funcion."""
        self.radioButtons = {}
        radioButtonsLayout = QGridLayout()
        self.radioButtons = {
            self.listSantander[0]: (0, 0),
            self.listSantanderDuplicated[0]: (0, 0),
            self.listSantander[1]: (1, 0),
            self.listSantanderDuplicated[1]: (1, 0),
            self.listSantander[2]: (2, 0),
            self.listSantanderDuplicated[2]: (2, 0),
            self.listSantander[3]: (3, 0),
            self.listSantanderDuplicated[3]: (3, 0),
            self.listSantander[4]: (4, 0),
            self.listSantanderDuplicated[4]: (4, 0),
            self.listSantander[5]: (5, 0),
            self.listSantanderDuplicated[5]: (5, 0),
            self.listSantander[6]: (6, 0),
            self.listSantanderDuplicated[6]: (6, 0),
            self.listSantander[7]: (7, 0),
            self.listSantanderDuplicated[7]: (7, 0),
            self.listSantander[8]: (8, 0),
            self.listSantanderDuplicated[8]: (8, 0),
            self.listSantander[9]: (9, 0),
            self.listSantanderDuplicated[9]: (9, 0),
            self.listSantander[10]: (0, 1),
            self.listSantanderDuplicated[10]: (0, 1),
            self.listSantander[11]: (1, 1),
            self.listSantanderDuplicated[11]: (1, 1),
            self.listSantander[12]: (2, 1),
            self.listSantanderDuplicated[12]: (2, 1),
            self.listSantander[13]: (3, 1),
            self.listSantanderDuplicated[13]: (3, 1),
            self.listSantander[14]: (4, 1),
            self.listSantanderDuplicated[14]: (4, 1),
            self.listSantander[15]: (5, 1),
            self.listSantanderDuplicated[15]: (5, 1),
            self.listSantander[16]: (6, 1),
            self.listSantanderDuplicated[16]: (6, 1),
            self.listSantander[17]: (7, 1),
            self.listSantanderDuplicated[17]: (7, 1),
            self.listSantander[18]: (8, 1),
            self.listSantanderDuplicated[18]: (8, 1),
            self.listSantander[19]: (9, 1),
            self.listSantanderDuplicated[19]: (9, 1),
        }
        numButtons = 0
        for btnText, pos in self.radioButtons.items():
            if numButtons % 2 == 0:
                self.radioButtons[btnText] = QLabel(self)
                pixmap = QPixmap(
                    '/home/alvaro/github/LaLigaEstadisticas/' + btnText + '.png')
                pixmap = pixmap.scaled(82.64, 82.64)
                self.radioButtons[btnText].setPixmap(pixmap)
                radioButtonsLayout.addWidget(self.radioButtons[btnText],
                                             pos[0], pos[1])
            else:
                # self.radioButtons2[btnText] = QRadioButton(btnText)
                self.radioButtons[btnText] = QRadioButton("")
                self.radioButtons[btnText].setFixedSize(140, 70)
                self.radioButtons[btnText].setChecked(False)
                radioButtonsLayout.addWidget(self.radioButtons[btnText],
                                             pos[0], pos[1])
                self.radioButtons[btnText].clicked.connect(partial
                                                           (self._drawSantander,
                                                            btnText[:-1]))
            numButtons += 1
        self.layout.addLayout(radioButtonsLayout, 1, 0)
        self._radioButtonState = True

    def _createRadioButton2(self):
        """Este es el docstring de la funcion."""
        self.radioButtons2 = {}
        radioButtons2Layout = QGridLayout()
        self.radioButtons2 = {
            self.listSmartbank[0]: (0, 0),
            self.listSmartbankDuplicated[0]: (0, 0),
            self.listSmartbank[1]: (1, 0),
            self.listSmartbankDuplicated[1]: (1, 0),
            self.listSmartbank[2]: (2, 0),
            self.listSmartbankDuplicated[2]: (2, 0),
            self.listSmartbank[3]: (3, 0),
            self.listSmartbankDuplicated[3]: (3, 0),
            self.listSmartbank[4]: (4, 0),
            self.listSmartbankDuplicated[4]: (4, 0),
            self.listSmartbank[5]: (5, 0),
            self.listSmartbankDuplicated[5]: (5, 0),
            self.listSmartbank[6]: (6, 0),
            self.listSmartbankDuplicated[6]: (6, 0),
            self.listSmartbank[7]: (7, 0),
            self.listSmartbankDuplicated[7]: (7, 0),
            self.listSmartbank[8]: (8, 0),
            self.listSmartbankDuplicated[8]: (8, 0),
            self.listSmartbank[9]: (9, 0),
            self.listSmartbankDuplicated[9]: (9, 0),
            self.listSmartbank[10]: (10, 0),
            self.listSmartbankDuplicated[10]: (10, 0),
            self.listSmartbank[11]: (0, 1),
            self.listSmartbankDuplicated[11]: (0, 1),
            self.listSmartbank[12]: (1, 1),
            self.listSmartbankDuplicated[12]: (1, 1),
            self.listSmartbank[13]: (2, 1),
            self.listSmartbankDuplicated[13]: (2, 1),
            self.listSmartbank[14]: (3, 1),
            self.listSmartbankDuplicated[14]: (3, 1),
            self.listSmartbank[15]: (4, 1),
            self.listSmartbankDuplicated[15]: (4, 1),
            self.listSmartbank[16]: (5, 1),
            self.listSmartbankDuplicated[16]: (5, 1),
            self.listSmartbank[17]: (6, 1),
            self.listSmartbankDuplicated[17]: (6, 1),
            self.listSmartbank[18]: (7, 1),
            self.listSmartbankDuplicated[18]: (7, 1),
            self.listSmartbank[19]: (8, 1),
            self.listSmartbankDuplicated[19]: (8, 1),
            self.listSmartbank[20]: (9, 1),
            self.listSmartbankDuplicated[20]: (9, 1),
            self.listSmartbank[21]: (10, 1),
            self.listSmartbankDuplicated[21]: (10, 1),
        }
        numButtons = 0
        for btnText, pos in self.radioButtons2.items():
            if numButtons % 2 == 0:
                self.radioButtons2[btnText] = QLabel(self)
                pixmap = QPixmap(
                    '/home/alvaro/github/LaLigaEstadisticas/' + btnText + '.png')
                pixmap = pixmap.scaled(82.64, 82.64)
                self.radioButtons2[btnText].setPixmap(pixmap)
                radioButtons2Layout.addWidget(self.radioButtons2[btnText],
                                              pos[0], pos[1])
            else:
                # self.radioButtons2[btnText] = QRadioButton(btnText)
                self.radioButtons2[btnText] = QRadioButton("")
                self.radioButtons2[btnText].setFixedSize(140, 70)
                self.radioButtons2[btnText].setChecked(False)

                radioButtons2Layout.addWidget(self.radioButtons2[btnText],
                                              pos[0], pos[1])
                self.radioButtons2[btnText].clicked.connect(partial
                                                            (self._drawSmartbank,
                                                             btnText[:-1]))
                # self._radioButton.toggled.connect(lambda:
                #                                   self.btnstate(self._radioButton))
            numButtons += 1
        self.layout.addLayout(radioButtons2Layout, 1, 0)
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
            # print("Campeonato seleccionado: ", self._box.currentText())
            if self._box.currentText() == "Liga Santander":
                self._clearRadioButtons()
                self._createRadioButton()
            elif self._box.currentText() == "Liga Smartbank":
                self._clearRadioButtons()
                self._createRadioButton2()

    def _drawSantander(self, btnText):
        graphic = GraphicExcel(self.sheet, btnText,
                               self.maxClubsSantander, self.firstRowSantander, self.dictCommentsSantander[btnText])
        toolbar = NavigationToolbar(graphic, self)
        self.layout.addWidget(toolbar, 0, 1)
        self.layout.addWidget(graphic, 1, 1)
        # self.show()

        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(toolbar)
        # widget = QWidget()
        # widget.setLayout(layout)
        # self.setCentralWidget(widget)
        # layout.addWidget(sc)

    def _drawSmartbank(self, btnText):
        graphic = GraphicExcel(self.sheet, btnText,
                               self.maxClubsSmartbank, self.firstRowSmartbank, self.dictCommentsSmartbank[btnText])
        toolbar = NavigationToolbar(graphic, self)
        self.layout.addWidget(toolbar, 0, 1)
        self.layout.addWidget(graphic, 1, 1)
