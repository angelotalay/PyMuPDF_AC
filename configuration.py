import json


# TODO: SET CONFIGURATION FOR REMOVALS
class Configuration:
    def __init__(self, config_path):
        self.title = None
        self.headers = None
        self.subheadings = None
        self.paragraphs = None
        self.removals = None
        self.config_path = config_path

    def read_configuration(self):
        with open(self.config_path, 'r') as file:
            json_object = json.load(file)
        self.title = json_object['title']
        self.headers = json_object['heading']
        self.subheadings = json_object['subheading']
        self.paragraphs = json_object['paragraph']

