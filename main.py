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
    #points = [0, -1, 0.35, 0.5, 0.75, 1.5, -1, -1.5, 0, 0.25]
    range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
    fig = plt.figure(num = None, figsize = (80, 3), dpi=80, facecolor = 'w', edgecolor = 'k')
    ax = fig.add_axes([0.0, 0.0, 1, 1])
    ax.scatter(range, points, color = 'b')
    fig.suptitle('test title')
    #fig.set_xlabel('categories')
    plt.xlabel('xlabel')
    plt.ylabel('ylabel')

    #plt.plot(range, points)

    plt.show()

    # Fake dataset
    height = [3, 12, 5, 18, 45]
    bars = ('A', 'B', 'C', 'D', 'E')
    y_pos = np.arange(len(bars))

    # Create bars and choose color
    plt.bar(y_pos, height, color = (0.5,0.1,0.5,0.6))

    # Add title and axis names
    plt.title('My title')
    plt.xlabel('categories')
    plt.ylabel('values')

    # Limits for the Y axis
    plt.ylim(0,60)

    # Create names
    plt.xticks(y_pos, bars)

    # Show graphic
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
