import xlsxwriter
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "client_secrets2.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Sheet").sheet1
list_of_lists = sheet.get_all_values()
workbook = xlsxwriter.Workbook('Quiniela Script.xlsx')
worksheet = workbook.add_worksheet()

row = 0

for col, data in enumerate(list_of_lists):
    worksheet.write_row(col, row, data)

workbook.close()
