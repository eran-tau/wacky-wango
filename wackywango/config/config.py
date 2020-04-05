from configparser import ConfigParser
import os
import pathlib
import ast

class Config:
    def __init__(self):
        path = os.environ.get('WACKYWANGO_CONFIG')
        self.config_parser = ConfigParser()
        if path:
            self.config_parser.read(path)
        else:
            root = pathlib.Path(__file__).parent.absolute()
            self.config_parser.read(root / 'config.ini')


    def __getattr__(self, item):
        return self.config_parser[item]

    def get_queue_keys(self):
        return ast.literal_eval(self.config_parser['server']['queue_keys'])
