#! /usr/bin/env python
import os
import jsonpickle
import time
import logging
import requests
from yapsy.PluginManager import PluginManager
from . import COLOURS

FORMAT = '%(asctime)-15s %(name)s [%(levelname)s]: %(message)s'
REQUEST_URL_FORMAT = '{protocol}://{host}:{port}{uri}'
THIS_DIR = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(format=FORMAT, level=logging.ERROR, datefmt="%Y-%m-%d %H:%M:%S")
LOG = logging.getLogger('smolder')
REQUESTS_LOG = logging.getLogger('requests')
REQUESTS_LOG.setLevel(logging.ERROR)
LOG.setLevel(logging.DEBUG)

logging.getLogger('yapsy').setLevel(logging.INFO)

manager = PluginManager()
manager.setPluginPlaces([THIS_DIR, "./.plugins"])
manager.collectPlugins()

class Charcoal(object):

    def __init__(self, **kwargs):
        self.passed = 0
        self.failed = 0
        self.test = kwargs['test']
        host = kwargs['host']
        inputs = self.test['inputs']
        self.formatters = {}
        inputs['url'] = REQUEST_URL_FORMAT.format(protocol=self.test['protocol'], host=host, port=self.test['port'], uri=self.test['uri'])
        self.inputs = inputs

        if not hasattr(self.test['inputs'], 'allow_redirects'):
            self.test['inputs']['allow_redirects'] = False
        if not hasattr(self.test['inputs'], 'timeout'):
            self.test['inputs']['timeout'] = 30
        if not hasattr(self.test['inputs'], 'verify'):
            self.test['inputs']['verify'] = False

        start = int(round(time.time() * 1000))
        self.req = getattr(requests, kwargs['test']['method'], 'get')(**inputs)
        end = int(round(time.time() * 1000))
        self.duration_ms = end - start

        self.output = self.test['name']
        self.output = "\n".join([self.output, self.__repr__()])
        if 'show_body' in self.test:
            self.output = "\n".join([self.output, self.req.content])

        # Trigger 'some action' from the loaded plugins
        for plugin_info in manager.getAllPlugins():
            if plugin_info.name in self.test['outcomes']:
                test_out = '  %10s: %s' % (plugin_info.name, plugin_info.plugin_object.run(self))
                self.output = "\n".join([self.output, test_out])


    def __str__(self):
        return self.output

    def __repr__(self):
        if hasattr(self, 'headers'):
            if self.inputs.headers != '':
                header_list = ['"{0}: {1}"'.format(k, v) for k, v in list(self.inputs.headers.items())]
                header = "-H " + (" -H ".join(header_list))
            else:
                header = self.inputs.headers
        else:
            header = ''
        if hasattr(self.inputs, 'data'):
            data = self.inputs.data
        else:
            data = ''
        #Adding curl output to allow simple debugging of the requests
        command = 'curl -v -s -o /dev/null {headers} -d {data} -X {method} "{uri}"'
        output = command.format(method=str(self.test['method']).upper(), headers=header, data=data, uri=self.inputs['url'])
        return output


    def pass_test(self, message):
        self.passed += 1
        status = "[PASS]"
        if getattr(self.test['outcomes'], "colour_output", True):
            status = COLOURS.to_green(status)
        return message + " " + status


    def fail_test(self, message):
        self.failed += 1
        status = "[FAIL]"
        if getattr(self.test['outcomes'], "colour_output", True):
            status = COLOURS.to_red(status)
        return message + " " + status


    def _to_json(self):
        return jsonpickle.encode(self)
