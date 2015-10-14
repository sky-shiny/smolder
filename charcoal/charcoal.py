#! /usr/bin/env python
import os
import time
import logging
import warnings
from copy import deepcopy
import jsonpickle
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

OUTPUT_WIDTH = 108


def deepupdate(original, update):
    """
    Recursively update a dict.
    Subdict's won't be overwritten but also updated.
    """
    for key, value in original.items():
        if not key in update:
            update[key] = value
        elif isinstance(value, dict):
            deepupdate(value, update[key])
    return update


class Charcoal(object):
    def __init__(self, test, host):
        """

        :rtype : object
        """

        self.passed = 0
        self.failed = 0

        LOG.debug("Test: {0}".format(test))
        test_defaults = dict(inputs=dict(allow_redirects=False, timeout=30), protocol="http", port=80, method="get",
                             outcomes=dict(expect_status_code=200))
        test_defaults["inputs"]["allow_redirects"] = False
        test_defaults["inputs"]["timeout"] = 30
        test_defaults["protocol"] = "http"
        test_defaults["port"] = 80
        test_defaults["method"] = "get"
        test_defaults["outcomes"]["expect_status_code"] = 200
        test_defaults["outcomes"]["colour_output"] = True
        final_dict = deepupdate(test_defaults, test)
        try:
            if type(final_dict["inputs"]["verify"]) == bool:
                self.verify = final_dict["inputs"]["verify"]
            elif final_dict["inputs"]["verify"] == "True":
                self.verify = True
            elif final_dict["inputs"]["verify"] == "False":
                self.verify = False
            elif type(final_dict["inputs"]["verify"]) == str:
                LOG.debug("Fucking requests having one argument which can accept input of multiple types")
                self.verify = final_dict["inputs"]["verify"]
            else:
                raise TypeError("Not sure what you want here")
            self.verify_specified = True
            del(final_dict["inputs"]["verify"])
        except (AttributeError, KeyError):
            if 'https' in final_dict['protocol']:
                self.verify = True
                self.verify_specified = False
            else:
                self.verify = False
                self.verify_specified = False
        self.test = deepcopy(final_dict)
        LOG.debug("Test with defaults: {0}".format(self.test))
        self.inputs = deepcopy(self.test['inputs'])
        request_url_format = '{protocol}://{host}:{port}{uri}'
        self.output = ("-" * OUTPUT_WIDTH)
        self.inputs['url'] = request_url_format.format(protocol=self.test['protocol'], host=host,
                                                       port=self.test['port'],
                                                       uri=self.test['uri'])
        LOG.debug("Testing {0}".format(self.inputs['url']))
        self.output = ("-" * OUTPUT_WIDTH)

        this_name = ("{0:^" + str(OUTPUT_WIDTH) + "}").format(self.test['name'][:OUTPUT_WIDTH])
        self.output = "\n".join([self.output, this_name])
        this_url = ("{0:^" + str(OUTPUT_WIDTH) + "}").format(self.inputs["url"][:OUTPUT_WIDTH])
        self.output = "\n".join([self.output, this_url])
        self.output = "\n".join([self.output, self.__repr__()])
        self.output = "\n".join([self.output, ("-" * OUTPUT_WIDTH)])
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                LOG.debug("Verify is a: {0}, with value: {1}".format(type(self.verify), self.verify))
                start = int(round(time.time() * 1000))
                self.req = getattr(requests, self.test['method'].lower())(verify=self.verify, **self.inputs)
                end = int(round(time.time() * 1000))
                self.duration_ms = end - start
            except Exception:
                warnings.simplefilter("ignore")
                start = int(round(time.time() * 1000))
                self.req = getattr(requests, self.test['method'].lower())(verify=self.verify, **self.inputs)
                end = int(round(time.time() * 1000))
                self.duration_ms = end - start
                if not self.verify_specified:
                    message, status = self.fail_test("Insecure request not ignored by inputs['verify']")
                    self.add_output("SecureRequest", message, status)
                else:
                    if self.verify:
                        message, status = self.fail_test("Insecure request made")
                        self.add_output("SecureRequest", message, status)
                    else:
                        message, status = self.warn_test("Insecure request made and ignored")
                        self.add_output("SecureRequest", message, status)

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
                    self.add_output(plugin_info.name, message, status)
                    manager.deactivatePluginByName(plugin_info.name)

        self.output = "\n".join([self.output, "\n"])

    def __str__(self):
        return self.output

    def __repr__(self):
        LOG.debug(self.inputs)
        if "headers" in self.inputs:
            if self.inputs["headers"] != '':
                header_list = ['"{0}: {1}"'.format(k, v) for k, v in list(self.inputs["headers"].items())]
                header = "-H " + (" -H ".join(header_list))
            else:
                header = self.inputs["headers"]
        else:
            header = ''
        if "data" in self.inputs:
            data = '-d' + str(self.inputs["data"])
        else:
            data = ''

        if not self.verify and self.test["protocol"] == "https":
            curl_insecure = '--insecure'
        else:
            curl_insecure = ''

        # Adding curl output to allow simple debugging of the requests
        command = 'curl {curl_insecure} -v -s -o /dev/null {headers} {data} -X {method} "{uri}"'
        output = command.format(method=str(self.test['method']).upper(), headers=header, data=data,
                                uri=self.inputs['url'], curl_insecure=curl_insecure)
        return output

    def pass_test(self, message):
        self.passed += 1
        status = "[PASS]"
        if self.test["outcomes"]["colour_output"]:
            status = COLOURS.to_green(status)
        return (message, status)

    def fail_test(self, message):
        self.failed += 1
        status = "[FAIL]"
        if self.test["outcomes"]["colour_output"]:
            status = COLOURS.to_red(status)
        return (message, status)

    def warn_test(self, message):
        self.passed += 1
        status = "[WARN]"
        if self.test["outcomes"]["colour_output"]:
            status = COLOURS.to_yellow(status)
        return (message, status)

    def add_output(self, name, message, status):
        test_out = name + ": " + message + "." * (OUTPUT_WIDTH - len(name) - len(message) - 8) + status.rjust(8)
        self.output = "\n".join([self.output, test_out])

    def _to_json(self):
        return jsonpickle.encode(self)
