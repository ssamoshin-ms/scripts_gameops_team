import json
from core.stages.prepare_data_google import PrepareDataFromGoogle
from core.stages.models.milestone_model import MilestoneModel, RewardModel
from core.stages.mappings import mapping_name_from_milestones_sheet as names_from_sheet


class ParserMilestonesFromOutputFile:

    def __init__(self, spread_sheet_id: str, prepare_data_from_google=PrepareDataFromGoogle):
        self.spread_sheet_id = spread_sheet_id
        self.sheet_name = names_from_sheet.sheet_name
        self.prepare_data_from_google = prepare_data_from_google
        self.response_error = {}
        self.response_data = {}

    def get_value_by_key_in_dict(self, key, dictionary):
        keys_list = list(dictionary.keys())
        if key in keys_list:
            value = dictionary[key]
            return value
        else:
            return None

    def check_spaces(self, value: str):
        if value.startswith(' ') or value.endswith(' '):
            return True
        else:
            return False


    def add_error(self, configuration_name, error):
        keys = list(self.response_error.keys())
        if configuration_name in keys:
            self.response_error[configuration_name].append(error)
        else:
            self.response_error[configuration_name] = [error]

    def parse_and_validate_data(self):
        data_from_google = self.prepare_data_from_google(self.spread_sheet_id, self.sheet_name).get_data_from_google()
        # print(data_from_google)

        for item in data_from_google:

            configuration_name = self.get_value_by_key_in_dict(names_from_sheet.configuration_name, item)
            if not configuration_name:
                error = {"configuration_name": "configuration_name field is empty"}
                self.add_error(configuration_name, error)
            elif self.check_spaces(configuration_name):
                error = {"configuration_name": "name starts or ends with space"}
                self.add_error(configuration_name, error)

            id = self.get_value_by_key_in_dict(names_from_sheet.id, item)
            if not id:
                error = {"id": "id field is empty"}
                self.add_error(configuration_name, error)
            elif self.check_spaces(id):
                error = {"id": "name starts or ends with space"}
                self.add_error(configuration_name, error)

            reward_tickets = self.get_value_by_key_in_dict(names_from_sheet.reward_tickets, item)
            if not reward_tickets:
                error = {id: "reward_tickets field is empty"}
                self.add_error(configuration_name, error)
            elif self.check_spaces(reward_tickets):
                error = {id: "reward_tickets starts or ends with space"}
                self.add_error(configuration_name, error)
            else:
                try:
                    ticket = int(reward_tickets.replace(',', ''))
                except:
                    error = {id: "reward_tickets has incorrect value"}
                    self.add_error(configuration_name, error)
                else:
                    if not ticket > 0:
                        error = {id: "reward_tickets has incorrect value"}
                        self.add_error(configuration_name, error)


            icon = self.get_value_by_key_in_dict(names_from_sheet.icon, item)
            if not icon:
                error = {id: "icon field is empty"}
                self.add_error(configuration_name, error)
            elif self.check_spaces(icon):
                error = {id: "icon starts or ends with space"}
                self.add_error(configuration_name, error)

            rewards_string = self.get_value_by_key_in_dict(names_from_sheet.reward, item)


            # parse reward
            rewards_objects_list = []
            rewards_list = rewards_string.split('\n')
            for reward_string in rewards_list:
                reward_list = reward_string.split('|')
                token_type_id = ''
                count = 0
                for i in reward_list:
                    reward_part = i.split(':')
                    # validate
                    try:
                        if len(reward_part) == 2:
                            if reward_part[0] == 'TokenTypeID':
                                if self.check_spaces(reward_part[1]):
                                    raise ValueError
                                elif len(reward_part[1]) == 0:
                                    raise ValueError
                                else:
                                    token_type_id = reward_part[1]
                            elif reward_part[0] == 'Count':
                                if self.check_spaces(reward_part[1]):
                                    raise ValueError
                                elif not int(reward_part[1]) > 0:
                                    raise ValueError
                                else:
                                    count = int(reward_part[1])
                            else:
                                raise ValueError
                        else:
                            raise ValueError
                    except:
                        error = {id: f"reward field has incorrect value"}
                        self.add_error(configuration_name, error)
                new_reward = RewardModel(token_type_id, count)
                rewards_objects_list.append(new_reward)

            milestone = MilestoneModel(id=id,
                             reward_tickets=reward_tickets,
                             icon=icon,
                             reward=rewards_objects_list)

            keys = list(self.response_data.keys())
            if configuration_name in keys:
                self.response_data[configuration_name].append(milestone)
            else:
                self.response_data[configuration_name] = [milestone]
        # print(self.response_data)
        # print(self.response_error)
        return self
