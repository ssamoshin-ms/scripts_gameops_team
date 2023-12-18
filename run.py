from core.stages.parser_tasks_from_output_file import ParserTasksFromOutputFile
from core.stages.parser_milestones_from_output_file import ParserMilestonesFromOutputFile

sheet_id = '1CH5954kzJdSA7mKL-3EpnPEEi1McmSd46yyc8YHAAG4'

# tasks = ParserTasksFromOutputFile(sheet_id)
# tasks.parse_and_validate_data()
# print()
# print(tasks.response_error)
# print()
# print(tasks.response_data)


milestones = ParserMilestonesFromOutputFile(sheet_id)
milestones.parse_and_validate_data()
print()
print(milestones.response_error)
print()
print(milestones.response_data)