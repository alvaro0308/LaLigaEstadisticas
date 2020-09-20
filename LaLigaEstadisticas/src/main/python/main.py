#!/usr/bin/env python3

# Filename: LaLigaEstadisticas.py

""" """

from openpyxl import load_workbook
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow

import sys, matplotlib.pyplot as plt, matplotlib.patches as mpatches, numpy as np, matplotlib.pyplot as mpl

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QComboBox
import functools

__version__ = "alpha"
__author__ = "Álvaro"

ERROR_MSG = "ERROR"


def printPoints(sheet, firstRow, firstCol, lastCol, maxClubs, gamesPlayed):
    pointsNew = [None] * gamesPlayed
    rangePoints = [None] * gamesPlayed
    for row in range(firstRow, maxClubs + firstRow):
        for value in sheet.iter_rows(min_row = row, max_row = row, min_col = firstCol,
                                    max_col = lastCol , values_only = True):
            if gamesPlayed == 1:
                points = value[0]
            else:
                points = value[0:gamesPlayed]

            print(points)
            checkGames(gamesPlayed)
            createLists(points, pointsNew, rangePoints, gamesPlayed)
            createGraphic(pointsNew, rangePoints, gamesPlayed)

def checkGames(gamesPlayed):
    if gamesPlayed == 1:
        print("Games played is equal to one, can't graphic it")
        sys.exit(1)

def createLists(points, pointsNew, rangePoints, gamesPlayed):
    temp = 0
    for i in range(0, gamesPlayed):
        pointsNew[i] = points[i] - 1.5 + temp
        temp = pointsNew[i]
    for j in range(1, gamesPlayed + 1):
        rangePoints[j - 1] = j

def createGraphic(pointsNew, rangePoints, gamesPlayed):

    mpl.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots(figsize = (10, 2))
    fig.tight_layout()
    fig.patch.set_facecolor('xkcd:gray')
    ax.scatter(rangePoints, pointsNew, color = 'b')
    ax.plot(rangePoints, pointsNew, color = 'k')
    ax.set_xlim(0, gamesPlayed)
    ax.set_facecolor('xkcd:gray')
    ax.set_yticklabels([])
    ax.set_ylabel('Puntuación', fontsize = 10)
    ax.set_xlabel('Jornadas', fontsize = 10)
    ax.set_title('Club\n')
    ax.grid(linestyle = '--', linewidth = 0.5)
    plt.show()

def main():
    workbook = load_workbook(filename = "Quiniela.xlsx")
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
    printPoints(sheet, firstRowSantander, firstCol, lastCol, maxClubsSantander, gamesPlayed)
    print("\nLiga Smartbank")
    printPoints(sheet, firstRowSmartbank, firstCol, lastCol, maxClubsSmartbank, gamesPlayed)

class Menu(QWidget):
   def __init__(self, parent = None):
      super(Menu, self).__init__(parent)

      layout = QHBoxLayout()
      self.cb = QComboBox()
      self.cb.addItems(["Liga Santander", "Liga Smartbank"])
      self.cb.currentIndexChanged.connect(self.selectionchange)

      layout.addWidget(self.cb)
      self.setLayout(layout)
      self.setWindowTitle("Menu Ligas")

   def selectionchange(self,i):
      for count in range(self.cb.count()):
         print(self.cb.itemText(count))
      print("Current index", i, "selection changed ", self.cb.currentText())

if __name__ == '__main__':
    #main()
    app = QApplication(sys.argv)
    window = Menu()
    window.show()
    sys.exit(app.exec_())
