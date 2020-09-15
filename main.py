#!/usr/bin/env python3
from openpyxl import load_workbook
import sys, matplotlib.pyplot as plt, matplotlib.patches as mpatches, numpy as np

def printPoints(sheet, firstRow, firstCol, lastCol, maxClubs, gamesPlayed):
    for row in range(firstRow, maxClubs + firstRow):
        for value in sheet.iter_rows(min_row = row, max_row = row, min_col = firstCol,
                                    max_col = lastCol , values_only = True):
            if gamesPlayed == 1:
                points = value[0]
            else:
                points = value[0:gamesPlayed]

            print(points)
            plot(points)

def plot(points):
    points = [3.0, 0, 0.25, 0.5, 0, 0.25, 3.0, 1.0, 2.5, 2, 3.0, 0, 0, 0.75, 3.0, 1.0, 0.25, 0.5, 0, 0.25, 3.0, 1.0, 3.0, 0, 0, 0.75, 3.0, 1.0, 0.25, 3.0, 1.0, 0.5, 2.5, 0.5, 0, 0, 0.75, 3.0]
    range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
    #fig = plt.figure(num = None, figsize = (80, 3), dpi=80, facecolor = 'w', edgecolor = 'k')
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 2.5)
    ax.scatter(range, points, color = 'b')
    ax.plot(range, points)
    ax.set_ylabel('Puntuación', fontweight = 'bold')
    ax.set_xlabel('Jornadas', fontweight = 'bold')
    ax.grid(True)
    ax.set_title('Club\n', fontsize = 14, fontweight = 'bold')
    plt.show()

def main():
    workbook = load_workbook(filename = "Quiniela.xlsx")
    workbook.sheetnames
    sheet = workbook.active

    maxClubsSantander = 20
    maxClubsSmartbank = 22
    firstRowSantander = 3
    firstRowSmartbank = 25
    firstCol = 6
    lastCol = 43

    gamesPlayed = 38

    print("Liga Santander")
    printPoints(sheet, firstRowSantander, firstCol, lastCol, maxClubsSantander, gamesPlayed)
    print("\nLiga Smartbank")
    printPoints(sheet, firstRowSmartbank, firstCol, lastCol, maxClubsSmartbank, gamesPlayed)


if __name__ == "__main__":
    main()
