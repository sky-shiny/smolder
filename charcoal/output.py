#!/usr/bin/env python
import json
from collections import defaultdict


class Output(defaultdict):

    def __init__(self, format=None):
        super(Output, self).__init__(msg='')
        self.format = format

    def __str__(self):
        if self.format == 'json':
            ret = json.dumps(self)
        else:
            ret = self['msg']
        return ret

    def __repr__(self):
        return str(self)

    def append(self, value, sec='msg'):
        if sec == 'msg':
            self['msg'] = self['msg'] + value + '\n'
        else:
            self[sec] = value
