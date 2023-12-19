import json
from core.stages.prepare_data_google import PrepareDataFromGoogle
from core.stages.models.task_model import TaskModel, TaskStagesModel, TaskParamsModel
from core.stages.mappings import mapping_name_from_tasks_sheet as names_from_sheet

class ParserTasksFromOutputFile:

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

    def check_stages_count(self, task_stages_objects_list):
        count = 0
        for i in task_stages_objects_list:
            new_count = int(i.count)
            if count < new_count:
                count = new_count
            else:
                return False
        return True

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

            task_type = self.get_value_by_key_in_dict(names_from_sheet.task_type, item)
            if not task_type:
                error = {id: "task_type field is empty"}
                self.add_error(configuration_name, error)
            elif self.check_spaces(task_type):
                error = {id: "task_type starts or ends with space"}
                self.add_error(configuration_name, error)
            elif task_type not in ['destroy_object', 'craft_start', 'item_get', 'to_shop', 'put_on_map',
                                   'interact_building', 'upgrade', 'arrive', 'feed_animal']:
                error = {id: f"task_type '{task_type}' has incorrect type"}
                self.add_error(configuration_name, error)

            task_params_string = self.get_value_by_key_in_dict(names_from_sheet.task_params, item)
            task_stages_string = self.get_value_by_key_in_dict(names_from_sheet.task_stages, item)

            text_loc_key = self.get_value_by_key_in_dict(names_from_sheet.text_loc_key, item)
            if not text_loc_key:
                error = {id: "text_loc_key field is empty"}
                self.add_error(configuration_name, error)
            elif self.check_spaces(text_loc_key):
                error = {id: "text_loc_key starts or ends with space"}
                self.add_error(configuration_name, error)

            icon = self.get_value_by_key_in_dict(names_from_sheet.icon, item)
            if not icon:
                error = {id: "icon field is empty"}
                self.add_error(configuration_name, error)
            elif self.check_spaces(icon):
                error = {id: "icon starts or ends with space"}
                self.add_error(configuration_name, error)

            map_string = self.get_value_by_key_in_dict(names_from_sheet.map, item)
            map_groups_string = self.get_value_by_key_in_dict(names_from_sheet.map_groups, item)

            map_list = []
            map_groups_list = []
            if (not map_string and not map_groups_string) or map_string and map_groups_string:
                error = {id: "pls, check fields map and map_group"}
                self.add_error(configuration_name, error)
            else:
                if map_string:
                    map_list = map_string.split(',')
                elif map_groups_string:
                    map_groups_list = map_groups_string.split(',')

            # parse task params
            task_params_objects_list = []
            task_params_list = task_params_string.split('\n')
            for task_param_string in task_params_list:
                task_param_list = task_param_string.split('|')
                param_type = ''
                param = ''
                for i in task_param_list:
                    param_part = i.split(':')
                    # validate
                    try:
                        if len(param_part) == 2:
                            if param_part[0] == 'Type':
                                if param_part[1] in ['string', 'sint32']:
                                    param_type = param_part[1]
                                else:
                                    raise ValueError
                            elif param_part[0] == 'Param':
                                if not self.check_spaces(param_part[1]):
                                    param = param_part[1]
                                else:
                                    raise ValueError
                            else:
                                raise ValueError
                        else:
                            raise ValueError
                    except:
                        error = {id: f"task_params has incorrect value"}
                        self.add_error(configuration_name, error)
                new_task_param = TaskParamsModel(param_type, param)
                task_params_objects_list.append(new_task_param)
            # print(task_params_objects_list)

            # parse task stages
            task_stages_objects_list = []
            task_stages_list = task_stages_string.split('\n')
            for task_stage_string in task_stages_list:
                task_stage_list = task_stage_string.split('|')
                count = 0
                score = 0
                for i in task_stage_list:
                    stage_part = i.split(':')
                    # validate
                    try:
                        if len(stage_part) == 2:
                            if stage_part[0] == 'Count':
                                if not self.check_spaces(stage_part[1]):
                                    count = int(stage_part[1])
                                else:
                                    raise ValueError
                            elif stage_part[0] == 'Score':
                                if not self.check_spaces(stage_part[1]):
                                    score = int(stage_part[1])
                                else:
                                    raise ValueError
                            else:
                                raise ValueError
                        else:
                            raise ValueError
                    except:
                        error = {id: f"task_stages has incorrect value"}
                        self.add_error(configuration_name, error)
                new_task_stage = TaskStagesModel(count, score)
                task_stages_objects_list.append(new_task_stage)
            # print(task_stages_objects_list)

            if not self.check_stages_count(task_stages_objects_list):
                error = {id: f"task_stages has incorrect count"}
                self.add_error(configuration_name, error)

            task = TaskModel(id=id,
                             task_type=task_type,
                             task_params=task_params_objects_list,
                             task_stages=task_stages_objects_list,
                             text_loc_key=text_loc_key,
                             icon=icon,
                             map=map_list,
                             map_groups=map_groups_list)
            keys = list(self.response_data.keys())
            if configuration_name in keys:
                self.response_data[configuration_name].append(task)
            else:
                self.response_data[configuration_name] = [task]
        # print(self.response_data)
        # print(self.response_error)
        return self
