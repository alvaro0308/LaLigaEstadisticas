#!/usr/bin/env python3
from openpyxl import load_workbook
import sys

def main():
    workbook = load_workbook(filename = "Quiniela.xlsx")
    workbook.sheetnames

    sheet = workbook.active
    print(sheet)

    print(sheet.title)

    print(sheet["A1"].value)
    for value in sheet.iter_rows(min_row=1, max_row=2, min_col=1, max_col=3, values_only = True):
        print(value)

if __name__ == "__main__":
    main()
