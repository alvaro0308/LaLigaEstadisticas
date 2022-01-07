"""AppUI.py"""


import sys
import gspread
from PyQt5 import sip
import xlsxwriter
from PyQt5 import QtCore
from functools import partial
from PyQt5.QtGui import QPixmap
from GraphicExcel import GraphicExcel
from oauth2client.service_account import ServiceAccountCredentials
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QRadioButton, QComboBox, QWidget, QGridLayout, QMainWindow, QLabel, QPushButton


class AppUI(QMainWindow):
    """App User Interface"""

    def __init__(self, sheet, listClubsSantander, listClubsSmartbank,
                 dictMistersSantander, dictMistersSmartbank, dictCommentsSantander,
                 dictCommentsSmartbank, maxClubsSantander, maxClubsSmartbank,
                 firstRowSantander, firstRowSmartbank,
                 dictStandingSantander, dictStandingSmartbank, params):
        """"""
        super().__init__()
        self.params = params
        self.scope = self.params['scope']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            self.params['path'] + self.params['keysPath'] + self.params['creds'], self.scope)
        self.client = gspread.authorize(self.creds)
        self.dictMistersSantander = dictMistersSantander
        self.dictMistersSmartbank = dictMistersSmartbank
        self.listSantander = listClubsSantander
        self.listSantanderImage = listClubsSantander.copy()
        for i in range(0, len(self.listSantanderImage)):
            self.listSantanderImage[i] += "2"
        self.listSmartbank = listClubsSmartbank
        self.listSmartbankImage = listClubsSmartbank.copy()
        for i in range(0, len(self.listSmartbankImage)):
            self.listSmartbankImage[i] += "2"
        self.dictCommentsSantander = dictCommentsSantander
        self.dictCommentsSmartbank = dictCommentsSmartbank
        self.maxClubsSantander = maxClubsSantander
        self.maxClubsSmartbank = maxClubsSmartbank
        self.firstRowSantander = firstRowSantander
        self.firstRowSmartbank = firstRowSmartbank
        self.dictStandingSantander = dictStandingSantander
        self.dictStandingSmartbank = dictStandingSmartbank

        self.layout = QGridLayout()
        self.sheet = sheet
        self.setMinimumSize(
            self.params['minimumWidthWindow'], self.params['minimumHeightWindow'])
        _centralWidget = QWidget()
        _centralWidget.setLayout(self.layout)
        self.setCentralWidget(_centralWidget)
        self.showMaximized()

        self._createChampionshipMenu()
        self._createDownloadButton()
        self._connectSignals()
        self._clubsSantanderButtonsState = False
        self._clubsButtonsSmartbankState = False

    def _createChampionshipMenu(self):
        """Create championship menu"""
        self._championshipMenu = QComboBox()
        self._championshipMenu.InsertAtTop
        self._championshipMenu.addItems(["Seleccione un campeonato",
                                         "Liga Santander", "Liga Smartbank"])
        self.setWindowTitle("LaLigaEstadisticas")
        self.layout.addWidget(self._championshipMenu, 0, 0)

    def _createDownloadButton(self):
        """Create download button"""
        self._downloadButton = QPushButton()
        self._downloadButton.setText("Actualizar base de datos")
        self.layout.addWidget(self._downloadButton, 5, 0)

    def _createClubsSantanderButtons(self):
        """Create Santander clubs buttons"""
        self.clubsSantanderButtons = {}
        clubsSantanderButtonsLayout = QGridLayout()
        self.clubsSantanderButtons = {
            self.listSantander[0]: (0, 0),
            self.listSantanderImage[0]: (0, 0),
            self.listSantander[1]: (1, 0),
            self.listSantanderImage[1]: (1, 0),
            self.listSantander[2]: (2, 0),
            self.listSantanderImage[2]: (2, 0),
            self.listSantander[3]: (3, 0),
            self.listSantanderImage[3]: (3, 0),
            self.listSantander[4]: (4, 0),
            self.listSantanderImage[4]: (4, 0),
            self.listSantander[5]: (5, 0),
            self.listSantanderImage[5]: (5, 0),
            self.listSantander[6]: (6, 0),
            self.listSantanderImage[6]: (6, 0),
            self.listSantander[7]: (7, 0),
            self.listSantanderImage[7]: (7, 0),
            self.listSantander[8]: (8, 0),
            self.listSantanderImage[8]: (8, 0),
            self.listSantander[9]: (9, 0),
            self.listSantanderImage[9]: (9, 0),
            self.listSantander[10]: (0, 1),
            self.listSantanderImage[10]: (0, 1),
            self.listSantander[11]: (1, 1),
            self.listSantanderImage[11]: (1, 1),
            self.listSantander[12]: (2, 1),
            self.listSantanderImage[12]: (2, 1),
            self.listSantander[13]: (3, 1),
            self.listSantanderImage[13]: (3, 1),
            self.listSantander[14]: (4, 1),
            self.listSantanderImage[14]: (4, 1),
            self.listSantander[15]: (5, 1),
            self.listSantanderImage[15]: (5, 1),
            self.listSantander[16]: (6, 1),
            self.listSantanderImage[16]: (6, 1),
            self.listSantander[17]: (7, 1),
            self.listSantanderImage[17]: (7, 1),
            self.listSantander[18]: (8, 1),
            self.listSantanderImage[18]: (8, 1),
            self.listSantander[19]: (9, 1),
            self.listSantanderImage[19]: (9, 1),
        }
        numButtons = 0

        for btnText, pos in self.clubsSantanderButtons.items():
            if numButtons % 2 == 0:
                self.clubsSantanderButtons[btnText] = QLabel(self)
                pixmap = QPixmap(
                    self.params['path'] + self.params['resourcesPath'] +
                    self.params['clubsPath'] + btnText + self.params['extensionImage'])
                pixmap = pixmap.scaled(
                    self.params['imageWidth'], self.params['imageHeight'])
                self.clubsSantanderButtons[btnText].setPixmap(pixmap)
                clubsSantanderButtonsLayout.addWidget(self.clubsSantanderButtons[btnText],
                                                      pos[0], pos[1])
            else:
                self.clubsSantanderButtons[btnText] = QRadioButton("")
                self.clubsSantanderButtons[btnText].setFixedSize(
                    self.params['buttonClubHeight'], self.params['buttonClubWidth'])
                self.clubsSantanderButtons[btnText].setChecked(False)
                clubsSantanderButtonsLayout.addWidget(self.clubsSantanderButtons[btnText],
                                                      pos[0], pos[1])
                self.clubsSantanderButtons[btnText].clicked.connect(partial
                                                                    (self._drawSantander,
                                                                     btnText[:-1]))
            numButtons += 1

        self.layout.addLayout(clubsSantanderButtonsLayout, 1, 0)
        self._clubsSantanderButtonsState = True

    def _createClubsSmartbankButtons(self):
        """Create Smartbank clubs buttons"""
        self.clubsSmarbankButtons = {}
        clubsSmartbankButtonsLayout = QGridLayout()
        self.clubsSmarbankButtons = {
            self.listSmartbank[0]: (0, 0),
            self.listSmartbankImage[0]: (0, 0),
            self.listSmartbank[1]: (1, 0),
            self.listSmartbankImage[1]: (1, 0),
            self.listSmartbank[2]: (2, 0),
            self.listSmartbankImage[2]: (2, 0),
            self.listSmartbank[3]: (3, 0),
            self.listSmartbankImage[3]: (3, 0),
            self.listSmartbank[4]: (4, 0),
            self.listSmartbankImage[4]: (4, 0),
            self.listSmartbank[5]: (5, 0),
            self.listSmartbankImage[5]: (5, 0),
            self.listSmartbank[6]: (6, 0),
            self.listSmartbankImage[6]: (6, 0),
            self.listSmartbank[7]: (7, 0),
            self.listSmartbankImage[7]: (7, 0),
            self.listSmartbank[8]: (8, 0),
            self.listSmartbankImage[8]: (8, 0),
            self.listSmartbank[9]: (9, 0),
            self.listSmartbankImage[9]: (9, 0),
            self.listSmartbank[10]: (10, 0),
            self.listSmartbankImage[10]: (10, 0),
            self.listSmartbank[11]: (0, 1),
            self.listSmartbankImage[11]: (0, 1),
            self.listSmartbank[12]: (1, 1),
            self.listSmartbankImage[12]: (1, 1),
            self.listSmartbank[13]: (2, 1),
            self.listSmartbankImage[13]: (2, 1),
            self.listSmartbank[14]: (3, 1),
            self.listSmartbankImage[14]: (3, 1),
            self.listSmartbank[15]: (4, 1),
            self.listSmartbankImage[15]: (4, 1),
            self.listSmartbank[16]: (5, 1),
            self.listSmartbankImage[16]: (5, 1),
            self.listSmartbank[17]: (6, 1),
            self.listSmartbankImage[17]: (6, 1),
            self.listSmartbank[18]: (7, 1),
            self.listSmartbankImage[18]: (7, 1),
            self.listSmartbank[19]: (8, 1),
            self.listSmartbankImage[19]: (8, 1),
            self.listSmartbank[20]: (9, 1),
            self.listSmartbankImage[20]: (9, 1),
            self.listSmartbank[21]: (10, 1),
            self.listSmartbankImage[21]: (10, 1),
        }
        numButtons = 0
        for btnText, pos in self.clubsSmarbankButtons.items():
            if numButtons % 2 == 0:
                self.clubsSmarbankButtons[btnText] = QLabel(self)
                pixmap = QPixmap(
                    self.params['path'] + self.params['resourcesPath'] +
                    self.params['clubsPath'] + btnText + self.params['extensionImage'])
                pixmap = pixmap.scaled(
                    self.params['imageWidth'], self.params['imageHeight'])
                self.clubsSmarbankButtons[btnText].setPixmap(pixmap)
                clubsSmartbankButtonsLayout.addWidget(self.clubsSmarbankButtons[btnText],
                                                      pos[0], pos[1])
            else:
                self.clubsSmarbankButtons[btnText] = QRadioButton("")
                self.clubsSmarbankButtons[btnText].setFixedSize(
                    self.params['buttonClubHeight'], self.params['buttonClubWidth'])
                self.clubsSmarbankButtons[btnText].setChecked(False)

                clubsSmartbankButtonsLayout.addWidget(self.clubsSmarbankButtons[btnText],
                                                      pos[0], pos[1])
                self.clubsSmarbankButtons[btnText].clicked.connect(partial
                                                                   (self._drawSmartbank,
                                                                    btnText[:-1]))
                # self._radioButton.toggled.connect(lambda:
                #                                   self.btnstate(self._radioButton))
            numButtons += 1
        self.layout.addLayout(clubsSmartbankButtonsLayout, 1, 0)
        self._clubsButtonsSmartbankState = True

    def _clearClubsButtons(self):
        """Clear all clubs buttons"""
        if self._clubsSantanderButtonsState:
            for btnText, pos in self.clubsSantanderButtons.items():
                sip.delete(self.clubsSantanderButtons[btnText])
            self._clubsSantanderButtonsState = False
        if self._clubsButtonsSmartbankState:
            for btnText, pos in self.clubsSmarbankButtons.items():
                sip.delete(self.clubsSmarbankButtons[btnText])
            self._clubsButtonsSmartbankState = False

    def _connectSignals(self):
        """Connect buttons and menu"""
        self._championshipMenu.currentIndexChanged.connect(
            self._printChampionshipMenu)
        self._downloadButton.clicked.connect(self._downloadSheet)

    def _printChampionshipMenu(self):
        """Print championship menu"""
        if self._championshipMenu.currentText() == "Seleccione un campeonato":
            self._clearClubsButtons()
        else:
            if self._championshipMenu.currentText() == "Liga Santander":
                self._clearClubsButtons()
                self._createClubsSantanderButtons()
            elif self._championshipMenu.currentText() == "Liga Smartbank":
                self._clearClubsButtons()
                self._createClubsSmartbankButtons()

    def restart(self):
        QtCore.QCoreApplication.quit()
        QtCore.QProcess.startDetached(sys.executable, sys.argv)

    def _downloadSheet(self):
        """Download Google Sheet"""
        sheet = self.client.open(self.params['nameDatabase']).sheet1
        allValues = sheet.get_all_values()
        workbook = xlsxwriter.Workbook(
            self.params['path'] + self.params['databasePath'] +
            self.params['nameDownloadedDatabase'] + self.params['extensionDatabase'])
        worksheet = workbook.add_worksheet()
        row = 0

        for col, data in enumerate(allValues):
            worksheet.write_row(col, row, data)

        workbook.close()
        self.restart()

    def _drawSantander(self, btnText):
        """Draw Liga Santander graphic"""
        standing = list(self.dictStandingSantander.keys()).index(btnText) + 1
        graphic = GraphicExcel(self.sheet, btnText,
                               self.maxClubsSantander, self.firstRowSantander,
                               self.dictMistersSantander[btnText], self.dictCommentsSantander[btnText],
                               self.params, "Santander", standing)
        toolbar = NavigationToolbar(graphic, self)
        self.layout.addWidget(toolbar, 0, 1)
        self.layout.addWidget(graphic, 1, 1)

    def _drawSmartbank(self, btnText):
        """Draw Liga Smartbank graphic"""
        standing = list(self.dictStandingSmartbank.keys()).index(btnText) + 1
        graphic = GraphicExcel(self.sheet, btnText,
                               self.maxClubsSmartbank, self.firstRowSmartbank,
                               self.dictMistersSmartbank[btnText], self.dictCommentsSmartbank[btnText],
                               self.params, "Smartbank",  standing)
        toolbar = NavigationToolbar(graphic, self)
        self.layout.addWidget(toolbar, 0, 1)
        self.layout.addWidget(graphic, 1, 1)
