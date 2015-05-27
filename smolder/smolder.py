#! /usr/bin/env python
import os
import json
import sys
import socket
import time
import jinja2
import dpath.util
import requests
from requests.auth import HTTPBasicAuth
import random
from retrying import retry

FORMAT = '%(asctime)-15s %(name)s [%(levelname)s]: %(message)s'
import logging
import argh
from argh import arg, dispatch_command

logging.basicConfig(format=FORMAT, level=logging.ERROR, datefmt="%Y-%m-%d %H:%M:%S")
logging.getLogger('requests').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
LOG = logging.getLogger('smolder')
LOG.setLevel(logging.INFO)
PARSER = argh.ArghParser()

OUTPUT_WIDTH = 90
TEST_LINE_FORMAT = "{0:.<" + str(OUTPUT_WIDTH - 10) + "s} {1:4s}"
failed_tests = 0
passed_tests = 0


class colours:
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'


def fail_test(message):
    global failed_tests
    failed_tests += 1
    status = "[FAIL]"
    if 'GO_REVISION' not in os.environ:
        status = colours.RED + status + colours.RESET
    LOG.info(TEST_LINE_FORMAT.format(message + " ", status))


def pass_test(message):
    global passed_tests
    passed_tests += 1
    status = "[PASS]"
    if 'GO_REVISION' not in os.environ:
        status = colours.GREEN + status + colours.RESET
    LOG.info(TEST_LINE_FORMAT.format(message + " ", status))


def noop_test():
    """
    A no op test that simply returns true
    :return: True

    """
    LOG.info("Running no op test that should be replaced with something useful.")
    pass_test("Passed a no op test. Should be replaced with something useful.")
    return True


# TODO: Do a tcp_test before an http_test since the first is required
# for the second to work. So we would always run the tcp_test and
# follow up with the http test if the protocol was http
def run_test(test, host, force):
    """Run either HTTP or TCP test."""
    LOG.info("")
    LOG.info("{0:-^87s}".format(" " + test['name'] + " "))
    if test['protocol'].lower() == 'tcp':
        tcp_test(host, test['port'])
    elif test['protocol'].lower() == 'http':
        http_test(test, host, force)
    elif test['protocol'].lower() == 'https':
        http_test(test, host, force)
    elif test['protocol'].lower() == 'noop':
        noop_test()


@retry(wait_exponential_multiplier=500, wait_exponential_max=30000, stop_max_attempt_number=7)
def tcp_test(host, port):
    """Attempts to make a TCP socket connection on the specified host and
    port. Returns true if successful. Else returns false.

    """
    LOG.debug("TCP test called")
    try:
        my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_sock.settimeout(1)
        my_sock.connect((host, port))
        print("Connecting to {0} on port {1}....................[PASS]".format(host, port))
        my_sock.shutdown(2)
        my_sock.close()
    except socket.error:
        my_sock.close()
        LOG.debug("    Waiting for {0}:{1} to accept a connection".format(host, port))
        raise
    except Exception as error:
        LOG.debug("TCP test failed: {0}".format(error.message))
        raise


def curl_request(url, method, headers, data):
    # construct the curl command from request
    command = 'curl -v -s -o /dev/null {headers} {data} -X {method} "{uri}"'
    if headers != '':
        header_list = ['"{0}: {1}"'.format(k, v) for k, v in list(headers.items())]
        header = "-H " + (" -H ".join(header_list))
    else:
        header = headers
    output = command.format(method=method.upper(), headers=header, data=data, uri=url)
    LOG.info("\n{0}".format(output))


def http_test(test, host, force):
    """
    Make a request with the parameters defined in a test object.

    """
    url = '{0}://{1}:{2}{3}'.format(test['protocol'], host, test['port'], test['url'])
    curlurl = '{0}://{1}:{2}{3}'.format(test['protocol'], host, test['port'], test['url'])
    LOG.info(("{0:^" + str(OUTPUT_WIDTH) + "}").format(url)[:OUTPUT_WIDTH - 2])
    LOG.info("-" * (OUTPUT_WIDTH - 3))
    args = {}
    args['url'] = url

    # SSL certificate management
    if 'protocol' in test and test['protocol'] == 'https':
        args['verify'] = False
        if 'validate_cert' in test:
            if test['validate_cert'] == "False":
                args['verify'] = False
            elif test['validate_cert'] == "True":
                args['verify'] = True
            else:
                LOG.error("validate_cert must be 'True', 'False' or absent (defaults to False)")
                sys.exit(7)
        if not args['verify']:
            requests.packages.urllib3.disable_warnings()

    # Check we have request headers
    if 'request_headers' in test:
        headers = test['request_headers']
        LOG.debug("    Getting {0} with headers".format(url))
        for header in headers:
            LOG.debug("        {0}: {1}".format(header, headers[header]))
        args['headers'] = headers
    else:
        LOG.debug('    Getting {0} with no specified headers'.format(url))

    if 'cookie' in test:
        cookie = test['cookie']
        LOG.debug("    Adding cookie: {0}".format(cookie))
        args['cookies'] = dict(cookie)
    else:
        LOG.debug('    Getting {0} with no specified cookie'.format(url))

    # Do we need to authorise?
    if 'username' in test and 'password' in test:
        username = test['username']
        password = test['password']
        curlurl = '{0}://{1}:{2}@{3}:{4}{5}'.format(test['protocol'], username, password, host, test['port'],
                                                    test['url'])
        args['auth'] = HTTPBasicAuth(username, password)
        LOG.debug("    Using HttpBasicAuth {0}:{1}".format(username, '*' * len(password)))
    else:
        LOG.debug("    No auth required {0}".format(url))

    # Do we need to post data?
    if 'data' in test:
        LOG.debug("    Request data: {0}".format(test['data']))
        data = str(json.dumps(test['data']))
        args['data'] = data
    else:
        LOG.debug("    No data to post/put")

    # Do we need to send files?
    if 'file' in test:
        LOG.debug("    Request file: {0}".format(test['file']))
        data = (str(json.dumps(test['files']['filename'])), str(json.dumps(test['files']['content'])))
        args['files'] = data
    else:
        LOG.debug("    No data to post/put")

    # By default we only allow GET tests as we don't want to allow a test to
    # PUT or POST data since we don't want to change live data in the course
    # of testing. We can override this behaviour by using the --force

    if 'method' in test and (test['method'] != 'get') and not force:
        LOG.error("    Only GET requests allowed for testing: To override use --force")
        sys.exit(4)
    elif 'method' not in test:
        test['method'] = 'get'
    #We want to be explicit about each redirect.  If you want to test end to end write one for the redirect and one for the following location
    args['allow_redirects'] = False

    LOG.debug("requests arguments: {0}".format(args))

    #Adding curl output to allow simple debugging of the requests
    if 'data' in args and 'headers' in args:
        curl_request(curlurl, test['method'], args['headers'], args['data'])
    elif 'data' in args:
        curl_request(curlurl, test['method'], '', args['data'])
    elif 'headers' in args:
        curl_request(curlurl, test['method'], args['headers'], '')
    else:
        curl_request(curlurl, test['method'], '', '')

    # Make the request and time it
    start = int(round(time.time() * 1000))
    req = getattr(requests, test['method'], 'get')(**args)
    end = int(round(time.time() * 1000))
    duration_ms = end - start
    LOG.info('Request took {0}ms'.format(duration_ms))

    if 'response_header_values' in test:
        for header in test['response_header_values']:
            if header not in req.headers:
                fail_test("Expected header {0} not present".format(header))
            elif req.headers[header] != test['response_header_values'][header]:
                fail_test("Expecting {0}: {1}, got {2}: {3}".format(
                    header,
                    test['response_header_values'][header],
                    header,
                    req.headers[header]))
            else:
                pass_test("Header {0}: {1} present".format(header, req.headers[header]))

    if 'response_headers_present' in test:
        for header in test['response_headers_present']:
            if header not in req.headers:
                fail_test("Expected header {0} not present".format(header))
            else:
                pass_test("Header {0}: {1} present".format(header, req.headers[header]))

    if 'expect_status_code' in test:
        if 'response_redirect' in test and (
                        req.status_code == 301 or req.status_code == 302 or req.status_code == 307 or req.status_code == 308):
            LOG.debug("{0}".format(req.headers))
            if int(test['expect_status_code']) == req.status_code and test['response_redirect'] == req.headers[
                'location']:
                pass_test("Status code == {0} and redirect == {1}".format(test['expect_status_code'],
                                                                          test['response_redirect']))
            else:
                fail_test(
                    "Got status code {0} but got redirected to {1} instead of {2}".format(test['expect_status_code'],
                                                                                          req.headers['location'],
                                                                                          test['response_redirect']))
        else:
            if int(test['expect_status_code']) == req.status_code:
                pass_test("Status code == {0}".format(test['expect_status_code']))
            else:
                fail_test("Expecting status code {0} but got {1} instead".format(test['expect_status_code'],
                                                                                 str(req.status_code)))
    else:
        if req.status_code == 200:
            pass_test("Status code == 200")
        else:
            fail_test("Status code != 200: {0}".format(req.status_code))

    # Did we expect something specific in the response body?
    if 'response_body_contains' in test:
        required_text = test['response_body_contains']
        LOG.debug("Ensuring '{0}' appears in the response body".format(required_text))
        try:
            req_content = req.content.decode()
        except UnicodeDecodeError as error:
            req_content = req.content
        if required_text not in req_content:
            if 'show_body' in test:
                LOG.info("    Body: {0}".format(req.content))
            else:
                LOG.debug("    Body: {0}".format(req.content))
            fail_test("Body contains \"{0}\"".format(required_text))
        else:
            pass_test("Body contains \"{0}\"".format(required_text))
    else:
        LOG.debug("    No body content search requested")

    # Do we need to ensure something does NOT appear in the response body?
    if 'response_body_doesnt_contain' in test:
        banned_text = test['response_body_doesnt_contain']
        LOG.debug("Ensuring {0} doesn't appear in the body of the response".format(banned_text))
        try:
            req_content = req.content.decode()
        except UnicodeDecodeError as error:
            req_content = req.content
        if banned_text in req_content:
            LOG.debug("    Body: {0}".format(req.content))
            fail_test("Body contains \"{0}\" and shouldn't".format(banned_text))
        else:
            pass_test("Body doesn't contain \"{0}\"".format(banned_text))
    else:
        LOG.debug("No body content exclude search requested")

    # Check response time
    if 'response_max_time_ms' in test:
        if duration_ms > int(test['response_max_time_ms']):
            longer_by_ms = duration_ms - int(test['response_max_time_ms'])
            fail_test('Response time was {0}ms longer than {1}ms max ({2}ms)'.format(str(longer_by_ms),
                                                                                     test['response_max_time_ms'],
                                                                                     str(duration_ms)))
        else:
            shorter_by_ms = int(test['response_max_time_ms']) - duration_ms
            pass_test('Response time was {0}ms shorter than max ({1}ms)'.format(str(shorter_by_ms), str(duration_ms)))

    # Validate presence of partial dicts in response json
    if 'response_json_contains' in test:
        for path in list(test['response_json_contains'].keys()):
            expected_value = test['response_json_contains'][path]
            actual_value = dpath.util.search(req.json(), path)[path]
            if expected_value == actual_value:
                pass_test("Body contains expected json value at path \"{0}\"".format(path))
            else:
                fail_test(
                    "Invalid json value {0} at path \"{1}\", expecting {2}".format(actual_value, path, expected_value))
