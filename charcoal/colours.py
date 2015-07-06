#! /usr/bin/env python
class Colours(dict):
    def __init__(self):
        dict.__init__(dict(self))
        self.yellow = '\033[93m'
        self.green = '\033[92m'
        self.red = '\033[91m'
        self.reset = '\033[0m'

    def to_yellow(self, message):
        return self.yellow + message + self.reset

    def to_green(self, message):
        return self.green + message + self.reset

    def to_red(self, message):
        return self.red + message + self.reset

COLOURS = Colours()
