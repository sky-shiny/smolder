#!/usr/bin/env python2
import smolder
from smolder.charcoal import Charcoal
import yaml
import os
import logging
from nose.tools import raises
import httpretty

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
LOG = logging.getLogger('smolder')
LOG.setLevel(logging.DEBUG)


def test_github_status():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/github_status.json')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = smolder.charcoal.Charcoal(test=test, host='status.github.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    assert total_failed_tests == 0


def test_github_status_expect_fail():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/harsh_github_status.json')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = smolder.charcoal.Charcoal(test=test, host='status.github.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    assert total_failed_tests > 0


@httpretty.activate
def test_validate_json():
    total_failed_tests = 0
    total_passed_tests = 0
    mytest = open(THIS_DIR + '/mocks/validate_json_response.json')
    json_response = yaml.load(mytest)
    httpretty.register_uri(httpretty.GET, "http://status.github.com/", body=json_response, content_type="application/json")

    myfile = open(THIS_DIR + '/validate_json.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = smolder.charcoal.Charcoal(test=test, host='status.github.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    assert total_failed_tests == 0


@httpretty.activate
def test_validate_json_fail():
    total_failed_tests = 0
    total_passed_tests = 0
    mytest = open(THIS_DIR + '/mocks/validate_json_response.json')
    json_response = yaml.load(mytest)
    httpretty.register_uri(httpretty.GET, "http://status.github.com/", body=json_response, content_type="application/json")
    myfile = open(THIS_DIR + '/validate_json.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test, host='status.github.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    assert total_failed_tests >= 0


def test_tcp_test():
    smolder.tcp_test('127.0.0.1', 22)  # Are you running an ssh server?


@raises(Exception)
def test_fail_tcp_test():
    smolder.tcp_test('127.0.0.1', 4242)
