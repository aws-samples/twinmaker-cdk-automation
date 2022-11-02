import yaml
from os import path


class TwinMakerObject:
    def __init__(self, description: dict,parent=None) -> None:
        self.items = []
        self.parent = parent


class WindFarm(TwinMakerObject):
    def __init__(self, description: dict) -> None:
        super().__init__(description)
        self._description = description

        self.name = description['name'] if 'name' in description else None                

        if 'items' in description:
            for item in description['items']:
                self.items.append(self.build_item(item, self))


    def build_item(self, item_description: dict, parent=None)->TwinMakerObject:
        if not 'type' in item_description:
            raise Exception("No type defined for item")

        type = item_description['type']
        item = None
        if "TurbineGroup" == type:
            item = TurbineGroup(item_description, parent=parent)
        elif "Turbine" == type:
            item = Turbine(item_description, parent=parent)
        
        if "items" in item_description:
            for sub_item in item_description['items']:
                item.items.append(self.build_item(sub_item, parent=item))

        if item:
            return item
        else:
            raise Exception("Item type not found")

    def load_from_yaml(description_file_path: str):    
        if not path.exists(description_file_path):
            raise Exception(
                f"Path for site description not found: {description_file_path}"
            )

        with open(description_file_path) as file:
            description = yaml.load(file, Loader=yaml.FullLoader)
            return WindFarm(description)

class TurbineGroup(TwinMakerObject):
    def __init__(self, description: dict, parent=None) -> None:
        super().__init__(description,parent=parent)

        self.shape = description['shape'] if 'shape' in description else None
        self.width = description['width'] if 'width' in description else None
        self.diameter = description['diameter'] if 'diameter' in description else None




class Turbine(TwinMakerObject):
    def __init__(self, description: dict, parent=None) -> None:
        super().__init__(description,parent=parent)

        self.device_code = description['device_code'] if 'device_code' in description else None

        
