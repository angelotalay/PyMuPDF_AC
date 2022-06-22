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
            contents = file.readlines()
        config_dict = {}
        for line in contents:
            split = line.split(',')
            config_dict[split[0]] = {split[1]:split[2]}
        print(config_dict)
        self.title = config_dict['title']
        self.headers = config_dict['heading']
        self.subheadings = config_dict['subheading']
        self.paragraphs = config_dict['paragraph']

