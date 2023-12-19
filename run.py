from core.stages.service_json.parser_stages_json import ParserStagesFromJson


sheet_id = '1CH5954kzJdSA7mKL-3EpnPEEi1McmSd46yyc8YHAAG4'

# tasks = ParserTasksFromOutputFile(sheet_id)
# tasks.parse_and_validate_data()
# print()
# print(tasks.response_error)
# print()
# print(tasks.response_data)


# milestones = ParserMilestonesFromOutputFile(sheet_id)
# milestones.parse_and_validate_data()
# print()
# print(milestones.response_error)
# print()
# print(milestones.response_data)

# json_data = PrepareDataFromLocalJson('22222_ny23')
# print(json_data.configuration)

stages_data = ParserStagesFromJson('22222_ny23')
stages_data.parse_data()
