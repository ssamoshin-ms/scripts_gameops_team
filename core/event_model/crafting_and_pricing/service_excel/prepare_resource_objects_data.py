from core.event_model.crafting_and_pricing.service_excel.prepare_data_google import PrepareDataFromGoogle
from core.event_model.crafting_and_pricing.service_excel import mapping_name_from_sheet as mapping
import re

class PrepareResourceObjectsData:

    def __init__(self, spread_sheet_id: str, prepare_data_from_google=PrepareDataFromGoogle, sheet_name=mapping.sheet_name):
        self.spread_sheet_id = spread_sheet_id
        self.sheet_name = sheet_name
        self.prepare_data_from_google = prepare_data_from_google

        self.errors = {}
        self.response_data = {}

    @staticmethod
    def change_column_titles(title_list):
        titles = title_list
        for i, v in enumerate(titles):
            if v.strip() == mapping.icon:
                titles[i] = mapping.new_icon
            elif v.strip() == mapping.item_id:
                titles[i] = mapping.new_item_id
            elif v.strip() == mapping.resource_building_id:
                titles[i] = mapping.new_resource_building_id
            elif v.strip() == mapping.pickup_drop_amount:
                titles[i] = mapping.new_pickup_drop_amount
            elif v.strip() == mapping.energy_chopping_cost:
                titles[i] = mapping.new_energy_chopping_cost
            elif v.strip() == mapping.source:
                titles[i] = mapping.new_source
            elif v.strip() == mapping.time:
                titles[i] = mapping.new_time
            elif v.strip() == mapping.map_zone_start:
                titles[i] = mapping.new_map_zone_start
            elif v.strip() == mapping.object_amount_on_map:
                titles[i] = mapping.new_object_amount_on_map
            elif v.strip() == mapping.total_item_on_map:
                titles[i] = mapping.new_total_item_on_map
            elif v.strip() == mapping.energy_chopping_cost_item:
                titles[i] = mapping.new_energy_chopping_cost_item
            elif v.strip() == mapping.total_energy_spent:
                titles[i] = mapping.total_energy_spent
            elif v.strip() == mapping.skip_by_ruby_cost:
                titles[i] = mapping.new_skip_by_ruby_cost
            elif v.strip() == mapping.skip_by_energy:
                titles[i] = mapping.new_skip_by_energy
                titles[i + 1] = mapping.new_skip_by_energy_cost
            elif v.strip() == mapping.skip_by_ticket:
                titles[i] = mapping.new_skip_by_ticket
                titles[i + 1] = mapping.new_skip_by_ticket_cost
            elif v.strip() == mapping.ruby_item_cost:
                titles[i] = mapping.new_ruby_item_cost
        return titles

    @staticmethod
    def delete_extra_symbols(value):
        new_value = value.split(' ')
        new_value = new_value[0]
        new_value = new_value.replace(',', '')
        new_value = new_value.replace('.', '')
        new_value = new_value.replace('-', '')
        return new_value

    # @staticmethod
    # def get_value_by_key_in_dict(key, dictionary):
    #     try:
    #         value = dictionary[key]
    #     except KeyError:
    #         return None
    #     else:
    #         return value
    #
    # @staticmethod
    # def check_spaces(value: str) -> bool:
    #     if value.startswith(' ') or value.endswith(' '):
    #         return True
    #     else:
    #         return False
    #
    # @staticmethod
    # def check_stages_count(task_stages_objects_list):
    #     count = 0
    #     for i in task_stages_objects_list:
    #         new_count = int(i.count)
    #         if count < new_count:
    #             count = new_count
    #         else:
    #             return False
    #     return True
    #
    # def add_error(self, configuration_name, error):
    #     keys = list(self.errors.keys())
    #     if configuration_name in keys:
    #         if error not in self.errors[configuration_name]:
    #             self.errors[configuration_name].append(error)
    #     else:
    #         self.errors[configuration_name] = [error]

    def validate_data(self):
        data = self.parse_data()

        # check item name and proceed with valid data



        correct_item_data = []
        for row in data:
            if row['item_id'] in []:
                correct_item_data.append(row)


        # check source field and check necessary fields and values for this source



        print(data)
        return data

    def parse_data(self):
        data_from_google = self.prepare_data_from_google(self.spread_sheet_id, self.sheet_name).get_data_from_google()

        # find necessary area
        from_index = 0
        for index, value in enumerate(data_from_google):
            match = re.search(mapping.sheet_area, str(value))
            if match:
                from_index = index
                break

        array = data_from_google[from_index::]

        # change titles
        titles = self.change_column_titles(array[0])

        result = []
        for row in array[1::]:
            if row:
                obj = {}
                for index, v in enumerate(row):
                    if titles[index]:
                        value = v.strip()
                        new_value = self.delete_extra_symbols(value)
                        if new_value:
                            obj[titles[index]] = new_value
                        else:
                            obj[titles[index]] = None
                result.append(obj)
        return result


if __name__ == '__main__':
    sheet_id = '17Ut44Bu2a2rf8TJRo6iHRerGdLtZTWy04jSDi76kzBM'
    data = PrepareResourceObjectsData(sheet_id)
    data.validate_data()

