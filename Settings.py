import json


class Settings:
    '''A simple wrapper around the json module to read a settings file.'''

    def __init__(self, file):
        self.file = file
        self.contents = self.read()

    def read(self):
        with open(self.file, 'r') as f:
            contents = json.load(f)
        return contents
