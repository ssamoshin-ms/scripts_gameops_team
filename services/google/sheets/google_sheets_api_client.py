from googleapiclient.errors import HttpError
from services.google.sheets.google_api import GoogleApi


class GSheetsClient(GoogleApi):
    API_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self):
        super().__init__(api_name=self.API_NAME, api_version=self.API_VERSION, scope=self.SCOPES)

    def get_all_sheets(self, spread_sheet_id: str) -> dict:
        """
        :param spread_sheet_id: The ID of the spreadsheet to retrieve data from.
        :return: dict
        """
        return self.service.spreadsheets().get(spreadsheetId=spread_sheet_id).execute()

    def get_sheet(self, spread_sheet_id: str, range: str) -> dict:
        """
        :param spread_sheet_id: The ID of the spreadsheet to retrieve data from.
        :param range: The A1 notation or R1C1 notation of the range to retrieve values from.
                      For example, if the spreadsheet data in Sheet1 is: A1=1. range=Sheet1!A1:B2
        :return: dict
        """
        return self.service.spreadsheets().values().get(spreadsheetId=spread_sheet_id, range=range).execute()

    def append(self, spread_sheet_id: str, range: str, value_input_option, values: list):
        """
        :param spread_sheet_id: The ID of the spreadsheet to retrieve data from.
        :param range: The A1 notation or R1C1 notation of the range to retrieve values from.
                      For example, if the spreadsheet data in Sheet1 is: A1=1. range=Sheet1!A1:B2
        :param value_input_option: How the input data should be interpreted.
        :param values: list if values for adding to sheet [12,232,324,2342]
        :return: dict
        """

        return self.service.spreadsheets().values().append(spreadsheetId=spread_sheet_id, range=range,
                                                           valueInputOption=value_input_option.value,
                                                           body={"values": values}).execute()

    def update(self, spread_sheet_id: str, range: str, value_input_option, values: list):
        """
        :param spread_sheet_id: The ID of the spreadsheet to retrieve data from.
        :param range: The A1 notation or R1C1 notation of the range to retrieve values from.
                      For example, if the spreadsheet data in Sheet1 is: A1=1. range=Sheet1!A1:B2
        :param value_input_option: How the input data should be interpreted.
        :param values: list if values for adding to sheet [12,232,324,2342]
        :return: dict
        """

        return self.service.spreadsheets().values().update(spreadsheetId=spread_sheet_id, range=range,
                                                           valueInputOption=value_input_option.value,
                                                           body={"values": values}).execute()

    def check_sheet_accessibility(self, spread_sheet_id: str):
        try:
            self.service.spreadsheets().get(spreadsheetId=spread_sheet_id).execute()
        except HttpError as error:
            return f'Sheet is not available: {error.reason}'

