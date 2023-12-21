from core.stages.service_excel.prepare_data_google import PrepareDataFromGoogle
from core.stages.models.milestone_model import MilestoneModel, RewardModel
from core.stages.service_excel import mapping_name_from_milestones_sheet as mapping


class ParserMilestonesFromOutputFile:

    def __init__(self, spread_sheet_id: str, prepare_data_from_google=PrepareDataFromGoogle):
        self.spread_sheet_id = spread_sheet_id
        self.sheet_name = mapping.sheet_name
        self.prepare_data_from_google = prepare_data_from_google
        self.errors = {}
        self.response_data = {}

    @staticmethod
    def get_value_by_key_in_dict(key, dictionary):
        try:
            value = dictionary[key]
        except KeyError:
            return None
        else:
            return value

    @staticmethod
    def check_spaces(value: str) -> bool:
        if value.startswith(' ') or value.endswith(' '):
            return True
        else:
            return False

    def add_error(self, configuration_name, error):
        keys = list(self.errors.keys())
        if configuration_name in keys:
            self.errors[configuration_name].append(error)
        else:
            self.errors[configuration_name] = [error]

    def parse_and_validate_data(self):
        data_from_google = self.prepare_data_from_google(self.spread_sheet_id, self.sheet_name).get_data_from_google()
        for i in data_from_google:

            if not self.get_value_by_key_in_dict(mapping.configuration_name, i):
                configuration_name = 'empty_configuration_name'
                error = "configuration_name field is empty"
                self.add_error(configuration_name, error)
            else:
                configuration_name = self.get_value_by_key_in_dict(mapping.configuration_name, i)
                if self.check_spaces(configuration_name):
                    error = f"some configuration_name starts or ends with space"
                    self.add_error(configuration_name.strip(), error)

            if not self.get_value_by_key_in_dict(mapping.object_id, i):
                _id = 'empty_id'
                error = {_id: "some id field is empty"}
                self.add_error(configuration_name, error)
            else:
                _id = self.get_value_by_key_in_dict(mapping.object_id, i)
                if self.check_spaces(_id):
                    error = {_id: "name starts or ends with space"}
                    self.add_error(configuration_name, error)

            reward_tickets = self.get_value_by_key_in_dict(mapping.reward_tickets, i)
            if not reward_tickets:
                error = {_id: "reward_tickets field is empty"}
                self.add_error(configuration_name, error)
            elif self.check_spaces(reward_tickets):
                error = {_id: "reward_tickets starts or ends with space"}
                self.add_error(configuration_name, error)
            else:
                try:
                    ticket = int(reward_tickets.replace(',', ''))
                except ValueError:
                    error = {_id: "reward_tickets has incorrect value"}
                    self.add_error(configuration_name, error)
                else:
                    if ticket <= 0:
                        error = {_id: "reward_tickets has incorrect value"}
                        self.add_error(configuration_name, error)

            icon = self.get_value_by_key_in_dict(mapping.icon, i)
            if not icon:
                error = {_id: "icon field is empty"}
                self.add_error(configuration_name, error)
            elif self.check_spaces(icon):
                error = {_id: "icon starts or ends with space"}
                self.add_error(configuration_name, error)

            rewards_string = self.get_value_by_key_in_dict(mapping.reward, i)

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
                            if reward_part[0] == mapping.token_type_id:
                                if self.check_spaces(reward_part[1]):
                                    raise ValueError
                                elif len(reward_part[1]) == 0:
                                    raise ValueError
                                else:
                                    token_type_id = reward_part[1]
                            elif reward_part[0] == mapping.count:
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
                    except ValueError:
                        error = {_id: f"reward field has incorrect value"}
                        self.add_error(configuration_name, error)
                new_reward = RewardModel(token_type_id, count)
                rewards_objects_list.append(new_reward)

            milestone = MilestoneModel(id=_id,
                                       reward_tickets=ticket,
                                       icon=icon,
                                       reward=rewards_objects_list)

            keys = list(self.response_data.keys())
            if configuration_name in keys:
                self.response_data[configuration_name].append(milestone)
            else:
                self.response_data[configuration_name] = [milestone]
        return self


if __name__ == '__main__':
    sheet_id = '1CH5954kzJdSA7mKL-3EpnPEEi1McmSd46yyc8YHAAG4'
    milestones = ParserMilestonesFromOutputFile(sheet_id)
    milestones.parse_and_validate_data()
    print(milestones.errors)
    print()
    print(milestones.response_data)
