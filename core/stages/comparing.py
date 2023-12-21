from core.stages.service_excel.parser_tasks_output_file import ParserTasksFromOutputFile
from core.stages.service_excel.parser_milestones_output_file import ParserMilestonesFromOutputFile
from core.stages.service_json.parser_stages_json import ParserStagesFromJson


def compare_stages():

    # STEP-1: specify link
    print()
    link = input('Excel. Specify the link:\n').strip()
    link_array = link.split('/')
    sheet_id = link_array[5]

    # STEP-2: show errors from excel
    tasks_data = ParserTasksFromOutputFile(sheet_id)
    tasks_data.parse_and_validate_data()
    # print(tasks.errors)
    if len(tasks_data.errors) > 0:
        print('EXCEL TASKS ERRORS')
        task_errors = tasks_data.errors
        for segment, errors in task_errors.items():
            print(f"For segment - '{segment}':")
            for error in errors:
                print(f"- {error}")
            print()

    milestones_data = ParserMilestonesFromOutputFile(sheet_id)
    milestones_data.parse_and_validate_data()

    if len(milestones_data.errors) > 0:
        print('EXCEL MILESTONE ERRORS')
        milestones_errors = milestones_data.errors
        for segment, errors in milestones_errors.items():
            print(f"For segment - '{segment}':")
            for error in errors:
                print(f"- {error}")
            print()

    tasks_data = tasks_data.response_data
    milestone_data = milestones_data.response_data

    # STEP-3: compare score form excel
    print('EXCEL SCORE')
    for segment, tasks in tasks_data.items():
        tasks_score = 0
        for task in tasks:
            for i in task.task_stages:
                tasks_score = tasks_score + i.score
        if segment in milestone_data.keys():
            milestone_score = milestone_data[segment][-1].reward_tickets
            if milestone_score != tasks_score:
                print(f'For {segment} last reward ticket ({milestone_score}) not equal sum of tasks score ({tasks_score})')

    # STEP-4: specify event
    print()
    event = input('JSON. Specify name of event:\n').strip()

    # STEP-5: show errors from json
    stages_data = ParserStagesFromJson(event)
    stages_data.parse_data()
    if len(stages_data.errors) > 0:
        for i in stages_data.errors:
            print('JSON ERRORS')

            print(i)

    # STEP-5: compare amount of tasks between excel and json and
    # take one task from excel and try to find it in json for comparing

    def compare_excel_task_with_json_task(item_json, item_excel):
        value = ' '
        if item_json != item_excel:
            value = 'x'
        return value

    tasks_json = stages_data.tasks
    for segment, tasks in tasks_data.items():
        print()
        print(f"For segment '{segment}' amount tasks from EXCEL - {len(tasks)}, and amount tasks from JSON - {len(tasks_json)}")
        for task_excel in tasks:
            for task_json in tasks_json:
                if task_json.id == task_excel.id:

                    task_type = compare_excel_task_with_json_task(task_json.task_type, task_excel.task_type)
                    task_params = compare_excel_task_with_json_task(task_json.task_params, task_excel.task_params)
                    task_stages = compare_excel_task_with_json_task(task_json.task_stages, task_excel.task_stages)
                    text_loc_key = compare_excel_task_with_json_task(task_json.text_loc_key, task_excel.text_loc_key)
                    icon = compare_excel_task_with_json_task(task_json.icon, task_excel.icon)
                    map = compare_excel_task_with_json_task(task_json.map, task_excel.map)
                    map_groups = compare_excel_task_with_json_task(task_json.map_groups, task_excel.map_groups)

                    print(f'id: {task_excel.id} / task_type: {task_type} / icon: {icon} / task_params: {task_params} / task_stages: {task_stages} / text_loc_key: {text_loc_key} / maps: {map} / map_groups: {map_groups}')


if __name__ == '__main__':
    compare_stages()
