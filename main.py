
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

json = "/Users/samoshinsergey/.config/gcloud/application_default_credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SAMPLE_SPREADSHEET_ID = "1oPTbFe9KEXmTmddIaZW8kw_Ar65kArMwAO2RCGmlQlI"
SAMPLE_RANGE_NAME = "Sheet1!A1:Q4"

def run():

    creds = Credentials.from_authorized_user_file(json, SCOPES)
    print(creds.client_id)

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        print(sheet)
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).uri
        )
        print(dir(result))
        print(result)
        # values = result.get("values", [])
        # print(values)
    except HttpError as err:
        print(err)





if __name__ == '__main__':
    run()



