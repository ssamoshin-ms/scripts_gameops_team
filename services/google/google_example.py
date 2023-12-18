import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_sheets_api_client import GSheetsClient

# SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# SPREADSHEET_ID = '1XoOvCbzAlYB77O-w_vtzaAFZ03eHMLUioMqShwF4lrc'
# SAMPLE_RANGE_NAME = "Links"


def run():

    google_sheets_client = GSheetsClient()
    sheets = google_sheets_client.get_all_sheets('18-iAScbp434KhItXP2xzYRb-oyMZEQdHOotovAXq7jg')
    sheet = google_sheets_client.get_sheet('18-iAScbp434KhItXP2xzYRb-oyMZEQdHOotovAXq7jg', 'import@Tasks')
    print(sheets)
    print(sheet)


    # creds = None
    #
    # creds = Credentials.from_service_account_file('../../secrets/key.json', scopes=SCOPES)
    #
    # try:
    #     service = build("sheets", "v4", credentials=creds)
    #     sheet = service.spreadsheets()
    #     result = (
    #         sheet.values()
    #         .get(spreadsheetId=SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    #     )
    #     print(result)
    #     values = result.get("values", [])
    #     print(values)
    # except HttpError as err:
    #     print(err)





if __name__ == '__main__':
    run()
