import json
from core import configs


class PrepareDataFromLocalJson:

    def __init__(self, json_name, base_path=configs.json_base_path):
        self.json_path = base_path + json_name
        self.configuration = None

    def get_data_from_json(self):
        with open(self.json_path, 'r', encoding='utf8') as f:
            self.configuration = json.load(f)  # transform json to dict
