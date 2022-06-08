import json


# TODO: SET CONFIGURATION FOR REMOVALS
class Configuration:
    def __init__(self, config_path):
        self.title = None
        self.header = None
        self.subheading = None
        self.paragraph = None
        self.removals = None
        self.config_path = config_path

    def read_configuration(self):
        with open(self.config_path, 'r') as file:
            json_object = json.load(file)
        self.title = json_object['title']
        self.header = json_object['heading']
        self.subheading = json_object['subheading']
        self.paragraph = json_object['paragraph']
