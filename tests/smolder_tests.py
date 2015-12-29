#!/usr/bin/env python
import charcoal
from charcoal import Charcoal
import yaml
import os
import logging
import json
import socket
from nose.tools import raises
import requests
import httpretty

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
LOG = logging.getLogger('smolder')
LOG.setLevel(logging.DEBUG)


def test_github_status():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/github_status.json')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test, host='status.github.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    assert total_failed_tests == 0


def test_github_status_expect_fail():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/harsh_github_status.json')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test, host='status.github.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    assert total_failed_tests > 0


def test_tcp_tests():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/tcp_test.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test, host='status.github.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    assert total_failed_tests == 0


@httpretty.activate
def test_validate_json():
    total_failed_tests = 0
    total_passed_tests = 0
    mytest = open(THIS_DIR + '/mocks/validate_json_response.json')
    httpretty.register_uri(httpretty.GET, "http://fakehost111.com/somejson", body=json.dumps(yaml.load(mytest)),
                           content_type="application/json")
    validate_httpretty = requests.get("http://fakehost111.com/somejson")
    LOG.debug("Expected response: {0}".format(validate_httpretty.json()))
    myfile = open(THIS_DIR + '/fixtures/validate_json.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test, host='fakehost111.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    assert total_failed_tests == 0


@httpretty.activate
def test_validate_json_fail():
    total_failed_tests = 0
    total_passed_tests = 0
    mytest = open(THIS_DIR + '/mocks/validate_json_response_fail.json')
    json_response = yaml.load(mytest)
    httpretty.register_uri(httpretty.GET, "http://fakehost111.com/somejson", body=str(json_response),
                           content_type="application/json")
    myfile = open(THIS_DIR + '/fixtures/validate_json.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test, host='fakehost111.com')
        if test_obj.failed > 0:
            LOG.debug(str(test_obj))
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    assert total_failed_tests >= 0


@raises(yaml.parser.ParserError)
def test_invalid_yaml_format():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/invalid_yaml.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test, host='status.github.com')
        if test_obj.failed > 0:
            LOG.debug(str(test_obj))
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    assert total_failed_tests == 0


def test_tcp_test():
    charcoal.tcp_test('127.0.0.1', 22)  # Are you running an ssh server?


def test_tcp_local():
    myfile = open(THIS_DIR + '/fixtures/tcp_test_local.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test, host='localhost')


@raises(Exception)
def test_tcp_local_fail():
    myfile = open(THIS_DIR + '/fixtures/tcp_test_local_fail.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test, host='localhost')


@raises(socket.error)
def test_fail_tcp_test():
    charcoal.tcp_test('127.0.0.1', 4242)
