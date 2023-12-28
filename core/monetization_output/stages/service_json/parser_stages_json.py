from core.monetization_output.stages.service_json.prepare_data_local_json import PrepareDataFromLocalJson
from core.models.task_model import TaskModel, TaskStagesModel, TaskParamsModel
from core.models import MilestoneModel, RewardModel
from core.monetization_output.stages.service_json import mapping_name_from_json as mapping


class ParserStagesFromJson:

    def __init__(self, event_name, prepare_data_from_local_json=PrepareDataFromLocalJson):
        self.event_name = event_name
        self.prepare_data_from_local_json = prepare_data_from_local_json
        self.tasks = []
        self.milestones = []
        self.errors = []

    def parse_tasks_data(self, data):
        response = []
        for task in data:

            _id = task[mapping.object_id]
            task_type = task[mapping.task_type]
            task_params = task[mapping.task_params]
            task_stages = task[mapping.task_stages]
            text_loc_key = task[mapping.text_loc_key]
            icon = task[mapping.icon]
            map_list = []
            map_groups_list = []

            keys = list(task.keys())
            if (mapping.maps in keys) and (mapping.maps_groups not in keys):
                map_list = task[mapping.maps]
            elif (mapping.maps_groups in keys) and (mapping.maps not in keys):
                map_groups_list = task[mapping.maps_groups]
            else:
                error = f"maps for tasks - {_id} has incorrect values"
                self.errors.append(error)

            task_params_objects_list = []
            task_stages_objects_list = []

            for i in task_params:
                keys = list(i.keys())
                if mapping.param_string in keys:
                    param_type = mapping.string
                    param = i[mapping.param_string]
                    task_param_object = TaskParamsModel(param_type, param)
                    task_params_objects_list.append(task_param_object)
                elif mapping.param_sint in keys:
                    param_type = mapping.sint32
                    param = str(i[mapping.param_sint])
                    task_param_object = TaskParamsModel(param_type, param)
                    task_params_objects_list.append(task_param_object)
                else:
                    error = f"task_params for tasks - {_id} has incorrect values"
                    self.errors.append(error)

            for i in task_stages:
                try:
                    count = int(i[mapping.task_count])
                    score = int(i[mapping.score])
                except ValueError:
                    error = f"task_stages for tasks - {_id} has incorrect values"
                    self.errors.append(error)
                else:
                    task_stages_object = TaskStagesModel(count, score)
                    task_stages_objects_list.append(task_stages_object)

            task = TaskModel(id=_id,
                             task_type=task_type,
                             task_params=task_params_objects_list,
                             task_stages=task_stages_objects_list,
                             text_loc_key=text_loc_key,
                             icon=icon,
                             map=map_list,
                             map_groups=map_groups_list)
            response.append(task)
        # print(response)
        return response

    def parse_milestones_data(self, data):
        response = []
        for milestone in data:
            _id = milestone[mapping.object_id]
            reward_tickets = int(milestone[mapping.reward_tickets])
            rewards_string = milestone[mapping.reward][mapping.tokens]
            icon = milestone[mapping.icon]

            rewards_objects_list = []
            for i in rewards_string:
                try:
                    count = i[mapping.milestone_count]
                    token_type_id = i[mapping.token_type_id]
                except KeyError:
                    error = f"reward for tasks - {_id} has incorrect keys"
                    self.errors.append(error)
                else:
                    reward = RewardModel(token_type_id, count)
                    rewards_objects_list.append(reward)

            milestone = MilestoneModel(id=_id,
                                       reward_tickets=reward_tickets,
                                       icon=icon,
                                       reward=rewards_objects_list)
            response.append(milestone)
        # print(response)
        return response

    def parse_data(self):
        data_from_json = self.prepare_data_from_local_json(self.event_name).configuration
        self.tasks = self.parse_tasks_data(data_from_json[mapping.tasks])
        self.milestones = self.parse_milestones_data(data_from_json[mapping.milestones])


if __name__ == '__main__':
    stages_data = ParserStagesFromJson('23196_ny24')
    stages_data.parse_data()
    print(stages_data.tasks)
    print(stages_data.milestones)
    print(stages_data.errors)
