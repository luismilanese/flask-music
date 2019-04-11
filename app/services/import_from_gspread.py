import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from app import app 

if __name__ == "__main__":
    raise Exception("You don't run this script directly. Run it through the admin session of the web project.")

def importer():
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(app.config['GSPREAD_API_CERT'], scope)
    client = gspread.authorize(creds)

    sheet = client.open(app.config['GSPREAD_TITLE']).sheet1

    values = sheet.get_all_records()
    return values
    