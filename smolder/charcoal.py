#! /usr/bin/env python
import jsonpickle
import time
import logging
import dpath
import requests
from . import COLOURS
import inspect


FORMAT = '%(asctime)-15s %(name)s [%(levelname)s]: %(message)s'
OUTPUT_WIDTH = 90
TEST_LINE_FORMAT = "{0:.<" + str(OUTPUT_WIDTH - 10) + "s} {1:4s}"
REQUEST_URL_FORMAT = '{protocol}://{host}:{port}{uri}'


logging.basicConfig(format=FORMAT, level=logging.ERROR, datefmt="%Y-%m-%d %H:%M:%S")
LOG = logging.getLogger('smolder')
REQUESTS_LOG = logging.getLogger('requests')
REQUESTS_LOG.setLevel(logging.ERROR)
LOG.setLevel(logging.INFO)

_plugins = []

def class_decorator(cls):
    LOG.debug("Decorating class")
    for name, method in inspect.getmembers(cls, predicate=inspect.ismethod):
        if hasattr(method, "use_method"):
            # do something with the method and class
            cls.add_plugin(method)
    return cls

def plugin(view):
    LOG.debug("Decorating plugin")
    # mark the method as something that requires view's class
    view.use_method = True
    return view

def in_test(view):
    def func_wrapper(name):
        if name in view.test:
            return view(name)
        else:
            pass

@class_decorator
class Charcoal(object):

    def __init__(self, **kwargs):
        LOG.debug("Test received: {0}".format(kwargs['test']))
        self.passed = 0
        self.failed = 0
        self.test = kwargs['test']
        host = kwargs['host']
        inputs = self.test['inputs']
        inputs['url'] = REQUEST_URL_FORMAT.format(protocol=self.test['protocol'], host=host, port=self.test['port'], uri=self.test['uri'])
        self.inputs = inputs
        LOG.debug("Inputs: {0}".format(inputs))
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
        for run_plugin in _plugins:
            LOG.debug("Running plugin: {0}".format(run_plugin))
            text = run_plugin(self)
            if text is not None:
                self.output = "\n".join([self.output, text])

    @staticmethod
    def add_plugin(plug):
        _plugins.append(plug)


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

    # def __str__(self):
    #     output = ""
    #     LOG.debug("PLUGINS: {0}".format(self.plugins))
    #     if 'show_body' in self.test:
    #         output = "\n".join(output, self.req.content)
    #     for run_plugin in self.plugins:
    #         LOG.debug("Running plugin: {0}".format(run_plugin))
    #         text = run_plugin(self)
    #         if text is not None:
    #             output = output.join([text, "\n"])
    #     return output


    def pass_test(self, message):
        self.passed += 1
        status = "[PASS]"
        if getattr(self.test['outcomes'], "colour_output", True):
            COLOURS.to_green(status)
        return TEST_LINE_FORMAT.format(message + " ", status)


    def fail_test(self, message):
        self.failed += 1
        status = "[FAIL]"
        if getattr(self.test['outcomes'], "colour_output", True):
            COLOURS.to_red(status)
        return TEST_LINE_FORMAT.format(message + " ", status)


    def _to_json(self):
        return jsonpickle.encode(self)

    @in_test
    @plugin
    def headers_present(self):
        for header in self.test['response_headers_present']:
            if header not in self.req.headers:
                return self.fail_test("Expected header {0} not present".format(header))
            else:
                return self.pass_test("Header {0}: {1} present".format(header, self.req.headers[header]))


    @plugin
    def expect_status_code(self):
        if 'expect_status_code' in self.test['outcomes']:
            if int(self.test['outcomes']['expect_status_code']) == self.req.status_code:
                return self.pass_test("Status code == {0}".format(self.test['outcomes']['expect_status_code']))
            else:
                return self.fail_test("Expecting status code {0} but got {1} instead".format(self.test['outcomes']['expect_status_code'], str(self.req.status_code)))
        else:
            if self.req.status_code == 200:
                return self.pass_test("Status code == 200")
            else:
                return self.fail_test("Status code != 200: {0}".format(self.req.status_code))

    @in_test
    @plugin
    def response_redirect(self):
        LOG.debug("{0}".format(self.req.headers))
        if int(self.test['outcomes']['expect_status_code']) == self.req.status_code and self.test['outcomes']['response_redirect'] == self.req.headers['location']:
            message = self.pass_test("Status code == {0} and redirect == {1}".format(self.test['outcomes']['expect_status_code'], self.test['outcomes']['response_redirect']))
            return message
        else:
            return self.fail_test("Got status code {0} but got redirected to {1} instead of {2}".format(
                self.test['outcomes']['expect_status_code'],
                self.req.headers['location'],
                self.test['outcomes']['response_redirect']))

    @in_test
    @plugin
    def response_body_contains(self):
        # Did we expect something specific in the response body?
        required_text = self.test['outcomes']['response_body_contains']
        LOG.debug("Ensuring '{0}' appears in the response body".format(required_text))
        try:
            req_content = self.req.content.decode()
        except UnicodeDecodeError:
            req_content = self.req.content
        if required_text not in req_content:
            return self.fail_test("Body contains \"{0}\"".format(required_text))
        else:
            return self.pass_test("Body contains \"{0}\"".format(required_text))


    @in_test
    @plugin
    def response_body_doesnt_contain(self):
        # Do we need to ensure something does NOT appear in the response body?
        banned_text = self.test['outcomes']['response_body_doesnt_contain']
        LOG.debug("Ensuring {0} doesn't appear in the body of the response".format(banned_text))
        try:
            req_content = self.req.content.decode()
        except UnicodeDecodeError:
            req_content = self.req.content
        if banned_text in req_content:
            LOG.debug("    Body: {0}".format(req_content))
            return self.fail_test("Body contains \"{0}\" and shouldn't".format(banned_text))
        else:
            return self.pass_test("Body doesn't contain \"{0}\"".format(banned_text))


    @in_test
    @plugin
    def response_max_time_ms(self):
        # Check response time
        if self.duration_ms > int(self.test['outcomes']['response_max_time_ms']):
            longer_by_ms = self.duration_ms - int(self.test['outcomes']['response_max_time_ms'])
            return self.fail_test('Response time was {0}ms longer than {1}ms max ({2}ms)'.format(str(longer_by_ms), self.test['outcomes']['response_max_time_ms'], str(self.duration_ms)))
        else:
            shorter_by_ms = int(self.test['outcomes']['response_max_time_ms']) - self.duration_ms
            return self.pass_test('Response time was {0}ms shorter than max ({1}ms)'.format(str(shorter_by_ms), str(self.duration_ms)))


    @in_test
    @plugin
    def response_json_contains(self):
        # Validate presence of partial dicts in response json
        for path in list(self.test['outcomes']['response_json_contains'].keys()):
            expected_value = self.test['outcomes']['response_json_contains'][path]
            actual_value = dpath.util.search(self.req.json(), path)[path]
            if expected_value == actual_value:
                return self.pass_test("Body contains expected json value at path \"{0}\"".format(path))
            else:
                return self.fail_test("Invalid json value {0} at path \"{1}\", expecting {2}".format(actual_value, path, expected_value))


    @in_test
    @plugin
    def response_header_values(self):
        for header in self.test['outcomes']['response_header_values']:
            if header not in self.req.headers:
                return self.fail_test("Expected header {0} not present".format(header))
            elif self.req.headers[header] != self.test['outcomes']['response_header_values'][header]:
                return self.fail_test("Expecting {0}: {1}, got {2}: {3}".format(
                    header,
                    self.test['outcomes']['response_header_values'][header],
                    header,
                    self.req.headers[header]))
            else:
                return self.pass_test("Header {0}: {1} present".format(header, self.req.headers[header]))
