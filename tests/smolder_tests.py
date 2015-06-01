#!/usr/bin/env python2
import smolder
import nose
import json
import os
from nose.tools import raises

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def test_github_status():
    myfile = open(THIS_DIR + '/github_status.json')
    test_json = json.load(myfile)
    for test in test_json['tests']:
        test_obj = smolder.charcoal.Charcoal(test=test, host='status.github.com')
    assert test_obj.failed == 0

def test_github_status_response_time_expect_fail():
    myfile = open(THIS_DIR + '/harsh_github_status.json')
    test_json = json.load(myfile)
    for test in test_json['tests']:
        test_obj = smolder.charcoal.Charcoal(test=test, host='status.github.com')
    assert test_obj.failed > 0

def test_tcp_test():
    smolder.tcp_test('127.0.0.1', 22) #Are you running an ssh server?

@raises(Exception)
def test_fail_tcp_test():
    smolder.tcp_test('127.0.0.1', 4242)

