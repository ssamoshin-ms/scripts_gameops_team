from services.google.sheets.google_sheets_api_client import GSheetsClient


class PrepareDataFromGoogle:

    def __init__(self, spread_sheet_id: str, sheet_name: str, g_sheets_client=GSheetsClient):
        self.google_sheets_client = g_sheets_client()
        self.spread_sheet_id = spread_sheet_id
        self.sheet_name = sheet_name

    def get_data_from_google(self):
        try:
            info = self.google_sheets_client.get_all_sheets(self.spread_sheet_id)
        except:
            print("incorrect spread sheet id or you don't have permission for access to sheet \n(share access with 'gcpsa-clientautoqa-gdrive@melsoft-infra.iam.gserviceaccount.com')")
            return
        else:

            # checking spaces in sheets names
            sheets = info['sheets']
            incorrect_sheet_names = []
            for i in sheets:
                list_name: str = i['properties']['title']
                if list_name.startswith(' ') or list_name.endswith(' '):
                    incorrect_sheet_names.append(list_name)
            if len(incorrect_sheet_names) > 0:
                print(f'incorrect sheet name. pls, delete spaces in {incorrect_sheet_names}')
                return

            # checking sheet name in  all sheets names
            sheet_names = []
            for i in sheets:
                list_name: str = i['properties']['title']
                sheet_names.append(list_name)
            if self.sheet_name not in sheet_names:
                print(f'incorrect sheet name. we dont have {self.sheet_name} among sheets names')
                return

        try:
            data = self.google_sheets_client.get_sheet(self.spread_sheet_id, self.sheet_name)
        except:
            print(f'incorrect sheet name. we dont have {self.sheet_name} among sheets names')
        else:
            # print(data['values'])
            result = []
            for row in data['values'][1::]:
                obj = {}
                for index, value in enumerate(row):
                    obj[data['values'][0][index]] = value
                result.append(obj)
            return result


if __name__ == '__main__':
    sheet_id = '1iPuei0kaWLeSqiCOjh6mrKWJcwsMqVOAJ3lik2kXeqU'
    sheet_name = 'import@Milestones'
    data_from_google = PrepareDataFromGoogle(sheet_id, sheet_name).get_data_from_google()
    print(data_from_google)


