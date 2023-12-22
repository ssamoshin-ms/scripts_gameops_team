import json
from core import configs

stages_path = configs.json_base_path + configs.stages

class PrepareDataFromLocalJson:

    def __init__(self, event_name, base_path=stages_path):
        self.json_path = base_path
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

