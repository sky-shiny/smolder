#! /usr/bin/env python
import os
import time
import logging
import warnings
from copy import deepcopy
from ldap3 import Connection, Server, ANONYMOUS, SIMPLE, SYNC, ASYNC

import jsonpickle
import requests
import validictory
from yapsy.PluginManager import PluginManager

from . import COLOURS, get_verify, get_host_overrides, tcptest
from .output import Output

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

SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "uri": {
            "type": "string",
            "required": False
        },
        "port": {
            "type": "integer",
            "required": False
        },
        "inputs": {
            "type": "object",
            "required": False,
            "properties": {
                "headers": {"type": "any", "required": False},
                "username": {"type": "any", "required": False},
                "password": {"type": "any", "required": False},
                "cookie": {"type": "any", "required": False},
                "data": {"type": "any", "required": False},
                "file": {"type": "any", "required": False},
                "verify": {"type": "any", "required": False},
                "allow_redirects": {"type": "any", "required": False},
                "timeout": {"type": "any", "required": False},
                "proxies": {"type": "any", "required": False},
                "bind_dn": {"type": "any","required": False},
                "bind_pw": {"type": "any","required": False},
                "dn": {"type": "any","required": False},
                "attr_key": {"type": "any", "required": False}
            }
        },
        "outcomes": {
            "type": "object",
            "required": False
        },
        "protocol": {
            "type": "string",
            "required": False,
            "enum": ["tcp", "http", "https","ldap","ldaps"]
        },
        "method": {
            "type": "string",
            "required": False,
            "enum": ["GET", "get", "post", "POST", "put", "PUT", "delete", "DELETE", "option", "OPTION", "PURGE", "purge"]
        },
        "request_headers": {
            "type": "None",
            "required": False
        },
        "url": {"type": "None","required": False}
    }
}


def deepupdate(original, update):
    """
    Recursively update a dict.
    Subdict's won't be overwritten but also updated.
    :param update:
    :param original:
    """
    for key, value in original.items():
        if key not in update:
            update[key] = value
        elif isinstance(value, dict):
            deepupdate(value, update[key])
    return update


class Charcoal(object):
    def __init__(self, test, host, output_format=None):
        """

        :rtype : object
        """

        self.passed = 0
        self.failed = 0
        self.duration_ms = 0
        try:
            validictory.validate(test, SCHEMA)
            LOG.debug("Valid schema")
        except ValueError as error:
            LOG.error("Error, invalid test format: {0}.  Tests now use v0.2 format. v0.1 branch is still available."
                      .format(error))
            raise

        try:
            self.port = test["port"]
        except (AttributeError, KeyError):
            print("Warning: No port definition found in the first test, using port 80 as default.")
            try:
                if test["protocol"] == "https":
                    self.port = 443
                else:
                    self.port = 80
            except (AttributeError, KeyError):
                self.port = 80

        self.output = Output(output_format=output_format)
        LOG.debug("Test: {0}".format(test))
        

        test_defaults = dict(inputs=dict(allow_redirects=False, timeout=30),
                             method="get",
                             outcomes=dict(colour_output=True))

        if 'protocol' in test and test['protocol'] not in ['http','https']:
            test_defaults['outcomes']['expect_status_code'] = 200

        host_overrides = get_host_overrides.get_host_overrides(host, self.port)

        if host_overrides['hostname'] is not None:
            self.host = host_overrides['hostname']
        else:
            self.host = host
        intermediate_dict = deepupdate(test_defaults, host_overrides)

        final_dict = deepupdate(intermediate_dict, test)

        try:
            verify = final_dict["inputs"]["verify"]
        except (AttributeError, KeyError):
            verify = None
        try:
            proto = final_dict['protocol']
        except (AttributeError, KeyError):
            proto = None

        (self.verify, self.verify_specified) = get_verify.get_verify(verify, proto)

        self.test = deepcopy(final_dict)
        if "tcp_test" in test and test["tcp_test"]:
            try:
                tcptest.tcp_test(self.host, self.port)
                self.pass_test("Connecting to {0} on port {1}".format(self.host, self.port))
            except Exception:
                self.fail_test("Connecting to {0} on port {1}".format(self.host, self.port))

        LOG.debug("Test with defaults: {0}".format(self.test))
        if "verify" in self.test["inputs"]:
            del self.test["inputs"]["verify"]
        self.inputs = deepcopy(self.test['inputs'])
        request_url_format = '{protocol}://{host}:{port}{uri}'
        try:
            self.inputs['url'] = request_url_format.format(protocol=self.test['protocol'], host=self.host,
                                                           port=self.test['port'],
                                                           uri=self.test['uri'])
        except KeyError:
            self.inputs['url'] = request_url_format.format(protocol=self.test['protocol'], host=self.host,
                                                           port=self.test['port'],
                                                           uri='')
        LOG.debug("Testing {0}".format(self.inputs['url']))
        self.output.append("-" * OUTPUT_WIDTH)

        this_name = ("{0:^" + str(OUTPUT_WIDTH) + "}").format(self.test['name'][:OUTPUT_WIDTH])
        self.output.append(this_name)
        this_url = ("{0:^" + str(OUTPUT_WIDTH) + "}").format(self.inputs["url"][:OUTPUT_WIDTH])
        self.output.append(this_url)
        self.output.append(self.__repr__())
        self.output.append("-" * OUTPUT_WIDTH)
        self.output.append(self.inputs, sec='request_inputs')
        self.run()

    def run(self):
        with warnings.catch_warnings():
            try:
                LOG.debug("Verify is a: {0}, with value: {1}".format(type(self.verify), self.verify))
                if self.verify:
                    warnings.simplefilter("error", requests.exceptions.SSLError)
                start = int(round(time.time() * 1000))

                if self.test["protocol"] in ['http','https']:
                    self.req = requests.request(self.test['method'].upper(), verify=self.verify, **self.inputs)

                elif self.test["protocol"] in ['ldap','ldaps']:
                    
                    try:
                        port = int(self.test['port'])
                    except ValueError:
                        if self.test["protocol"] == 'ldap':
                            port = 389
                        else:
                            port = 636


                    # We're going to try hitting the LDAP server at an IP: Ignore the fact
                    # that this doesn't match the LDAP servers cert
                    # define the server
                    s = Server(self.host, port=port, use_ssl=self.test['protocol']=='ldaps') 

                    # define the connection
                    c = Connection(s, user=self.inputs['bind_dn'], password=self.inputs['bind_pw'], read_only=True)

                    # perform the Bind operation
                    if not c.bind():
                        message, status = self.fail_test("Couldn't bind using dn=%s and password %s" % (self.inputs['bind_dn'], '*' * len(self.inputs['bind_pw'])), success=False)
                        return

                    self.req = c

                elif self.test["protocol"] == 'tcp':
                    try:
                        tcptest.tcp_test(self.host, self.port)
                        self.pass_test("Connecting to {0} on port {1}".format(self.host, self.port))
                    except Exception as error:
                        self.fail_test("Connecting to {0} on port {1}".format(self.host, self.port))

                end = int(round(time.time() * 1000))
                self.duration_ms = end - start
            except (RuntimeWarning, requests.exceptions.SSLError):

                if self.test["protocol"] in ['http','https']:
                    warnings.simplefilter("default", requests.exceptions.SSLError)
                    start = int(round(time.time() * 1000))
                    try:
                        self.req = requests.request(self.test['method'].upper(), verify=self.verify, **self.inputs)
                    except (requests.exceptions.SSLError) as e:
                        message, status = self.fail_test("Certificate verify failed and not ignored by inputs['verify']: %s" % (str(e)))
                        self.add_output("SSLVerify", message, status)
                        return
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



        # HTTP(s) TESTS
        if self.test["protocol"] in ['http','https']:
            self.output.append(dict(self.req.headers), sec='response_headers')
            self.output.append(self.req.status_code, sec='response_status_code')
            if 'show_body' in self.test:
                try:
                    req_content = self.req.content.decode()
                except UnicodeDecodeError:
                    req_content = self.req.content
                self.output.append(req_content)


        # Run plugins for everything exceot TCP tests
        if self.test["protocol"] != 'tcp':
            for plugin_info in manager.getAllPlugins():
                for outcome in self.test['outcomes']:
                    if plugin_info.name == outcome:
                        manager.activatePluginByName(plugin_info.name)
                        message, status = plugin_info.plugin_object.run(self)
                        self.add_output(plugin_info.name, message, status)
                        manager.deactivatePluginByName(plugin_info.name)

    def __str__(self):
        return str(self.output)

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


        output = ""
        
        # Adding curl output to allow simple debugging of the requests
        if self.test['protocol'] in ['http','https']:
            if not self.verify and self.test["protocol"] == "https":
                curl_insecure = '--insecure'
            else:
                curl_insecure = ''
            command = 'curl {curl_insecure} -v -s -o /dev/null {headers} {data} -X {method} "{uri}"'
            output = command.format(method=str(self.test['method']).upper(), headers=header, data=data, uri=self.inputs['url'], curl_insecure=curl_insecure)

        elif self.test['protocol'] in ['ldap','ldaps']:
            command = 'ldapsearch -LLL -D "{bind_dn}" -w "{bind_pw}" -H {protocol}://{hostname} -xb "{dn}" {attr}'
            output = command.format(bind_dn=self.test['inputs']['bind_dn'], bind_pw=self.test['inputs']['bind_pw'], protocol=self.test['protocol'], hostname=self.host, dn=self.test['inputs']['dn'], attr=self.test['inputs']['attr_key'])

        return output


    def pass_test(self, message):
        self.passed += 1
        status = "[PASS]"
        if self.test["outcomes"]["colour_output"]:
            status = COLOURS.to_green(status)
        return message, status

    def fail_test(self, message):
        self.failed += 1
        status = "[FAIL]"
        if self.test["outcomes"]["colour_output"]:
            status = COLOURS.to_red(status)
        return message, status

    def warn_test(self, message):
        self.passed += 1
        status = "[WARN]"
        if self.test["outcomes"]["colour_output"]:
            status = COLOURS.to_yellow(status)
        return message, status

    def add_output(self, name, message, status):
        test_out = name + ": " + message + "." * (OUTPUT_WIDTH - len(name) - len(message) - 8) + status.rjust(8)
        self.output.append(test_out)

    def _to_json(self):
        return jsonpickle.encode(self)
