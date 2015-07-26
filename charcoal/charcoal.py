#! /usr/bin/env python
import os
import jsonpickle
import time
import logging
import warnings
import requests
from yapsy.PluginManager import PluginManager
from . import COLOURS

FORMAT = '%(asctime)-15s %(name)s [%(levelname)s]: %(message)s'
THIS_DIR = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(format=FORMAT, level=logging.ERROR, datefmt="%Y-%m-%d %H:%M:%S")
LOG = logging.getLogger('smolder')
REQUESTS_LOG = logging.getLogger('requests')
REQUESTS_LOG.setLevel(logging.ERROR)

logging.getLogger('yapsy').setLevel(logging.INFO)
manager = PluginManager()
manager.setPluginPlaces([THIS_DIR, "~/.smolder_plugins"])
manager.collectPlugins()

OUTPUT_WIDTH = 93

class Charcoal(object):
    def __init__(self, test, host):
        """

        :rtype : object
        """

        self.passed = 0
        self.failed = 0
        test_defaults = {'inputs': {}}
        host = host
        self.formatters = {}
        LOG.debug("Test: {0}".format(test))
        try:
            test_defaults['inputs']['allow_redirects'] = test['inputs']['allow_redirects']
        except (AttributeError, KeyError):
            test_defaults['inputs']['allow_redirects'] = False
        try:
            test_defaults['inputs']['timeout'] = test['inputs']['timeout']
        except (AttributeError, KeyError):
            test_defaults['inputs']['timeout'] = 30
        try:
            test_defaults['protocol'] = test["protocol"]
        except (AttributeError, KeyError):
            test_defaults['protocol'] = "http"
        try:
            test_defaults['inputs']['verify'] = test['inputs']['verify']
        except (AttributeError, KeyError):
            if 'https' in test_defaults['protocol']:
                test_defaults['inputs']['verify'] = True
            else:
                test_defaults['inputs']['verify'] = False
        try:
            test_defaults["port"] = test["port"]
        except (AttributeError, KeyError):
            test_defaults["port"] = 80
        try:
            test_defaults["method"] = test["method"]
        except (AttributeError, KeyError):
            test_defaults["method"] = "get"


        test.update(test_defaults)
        self.test = test.copy()
        LOG.debug("Test with defaults: {0}".format(self.test))
        inputs = self.test['inputs']
        request_url_format = '{protocol}://{host}:{port}{uri}'
        inputs['url'] = request_url_format.format(protocol=self.test['protocol'], host=host, port=self.test['port'], uri=self.test['uri'])
        LOG.debug("Testing {0}".format(inputs['url']))
        self.inputs = inputs
        self.output = ("-" * (OUTPUT_WIDTH))
        this_name = ("{0:^" + str(OUTPUT_WIDTH) + "}").format(self.test['name'][:OUTPUT_WIDTH])
        self.output = "\n".join([self.output, this_name])
        this_url = ("{0:^" + str(OUTPUT_WIDTH) + "}").format(self.inputs["url"][:OUTPUT_WIDTH])
        self.output = "\n".join([self.output, this_url])
        self.output = "\n".join([self.output, self.__repr__()])
        self.output = "\n".join([self.output, ("-" * (OUTPUT_WIDTH))])
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                start = int(round(time.time() * 1000))
                self.req = getattr(requests, self.test['method'], 'get')(**inputs)
                end = int(round(time.time() * 1000))
                self.duration_ms = end - start
            except Exception:
                warnings.simplefilter("ignore")
                start = int(round(time.time() * 1000))
                self.req = getattr(requests, self.test['method'], 'get')(**inputs)
                end = int(round(time.time() * 1000))
                self.duration_ms = end - start
                if self.test['inputs']['verify']:
                    test_out = '%10s: %s' % ("SecureRequest", self.fail_test("Insecure request made"))
                    self.output = "\n".join([self.output, test_out])
                else:
                    test_out = '%10s: %s' % ("SecureRequest", self.fail_test("Insecure request made: add verify to your test['input']"))
                    self.output = "\n".join([self.output, test_out])

        if 'show_body' in self.test:
            try:
                req_content = self.req.content.decode()
            except UnicodeDecodeError:
                req_content = self.req.content
            self.output = "\n".join([self.output, req_content])

        for plugin_info in manager.getAllPlugins():
            for outcome in self.test['outcomes']:
                if plugin_info.name == outcome:
                    manager.activatePluginByName(plugin_info.name)
                    message, status = plugin_info.plugin_object.run(self)
                    test_out = plugin_info.name + ": " + message + "." * (
                    OUTPUT_WIDTH - len(plugin_info.name) - len(message) - 8) + status.rjust(8)
                    self.output = "\n".join([self.output, test_out])
                    manager.deactivatePluginByName(plugin_info.name)

        self.output = "\n".join([self.output, "\n"])

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
            data = '-d' + str(self.inputs.data)
        else:
            data = ''
        vfy = self.test['inputs']['verify']
        if not vfy:
            curl_insecure = '--insecure'
        else:
            curl_insecure = ''
        # Adding curl output to allow simple debugging of the requests
        command = 'curl {curl_insecure} -v -s -o /dev/null {headers} {data} -X {method} "{uri}"'
        output = command.format(method=str(self.test['method']).upper(), headers=header, data=data, uri=self.inputs['url'], curl_insecure=curl_insecure)
        return output

    def pass_test(self, message):
        self.passed += 1
        status = "[PASS]"
        if getattr(self.test['outcomes'], "colour_output", True):
            status = COLOURS.to_green(status)
        return (message, status)

    def fail_test(self, message):
        self.failed += 1
        status = "[FAIL]"
        if getattr(self.test['outcomes'], "colour_output", True):
            status = COLOURS.to_red(status)
            return (message, status)

    def _to_json(self):
        return jsonpickle.encode(self)
