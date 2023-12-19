import json


class PrepareDataFromLocalJson:

    def __init__(self, event_name):
        self.json_path = '/Users/samoshinsergey/project/family_island-defold-farm/.map-editor/jsons/stages/stages.json'
        self.event_name = event_name
        self.configuration = self.get_data_from_json()

    def get_data_from_json(self):
        with open(self.json_path, 'r', encoding='utf8') as f:
            data = json.load(f)  # transform json to dict
            # print(list(data['stages'].keys()))
        if self.event_name in list(data['stages'].keys()):  # check event in configs
            config = data['stages'][self.event_name]['configurations'][0]['configuration']
            return config
        else:
            return None

