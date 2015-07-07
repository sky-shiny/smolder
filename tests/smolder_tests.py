#!/usr/bin/env python2
import smolder
import yaml
import os
from nose.tools import assert_raises, raises
from imp import reload

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')

def test_noop_test():
  assert smolder.noop_test()


def test_github_status():
  myfile = open(os.path.join(FIXTURE_DIR, 'github_status.json'), 'rb')
  test_json = yaml.load(myfile)
  for test in test_json['tests']:
    smolder.http_test(test, 'status.github.com', False)
  reload(smolder)
  assert smolder.failed_tests == 0


def test_github_status_yaml_format():
    myfile = open(os.path.join(FIXTURE_DIR, 'github_status.yaml'), 'rb')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        smolder.http_test(test, 'status.github.com', False)
    reload(smolder)
    assert smolder.failed_tests == 0


def test_github_status_response_time_expect_fail():
  myfile = open(os.path.join(FIXTURE_DIR, 'harsh_github_status.json'), 'rb')
  test_json = yaml.load(myfile)
  for test in test_json['tests']:
    smolder.http_test(test, 'status.github.com', False)
  reload(smolder)
  assert smolder.failed_tests > 0


def test_github_status_response_time_expect_fail_yaml_format():
    myfile = open(os.path.join(FIXTURE_DIR, 'harsh_github_status.yaml'), 'rb')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        smolder.http_test(test, 'status.github.com', False)
    reload(smolder)
    assert smolder.failed_tests > 0

@raises(yaml.parser.ParserError)
def test_invalid_yaml_yaml_format():
    myfile = open(os.path.join(FIXTURE_DIR, 'invalid_yaml.yaml'), 'rb')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        smolder.http_test(test, 'status.github.com', False)
    reload(smolder)
    assert smolder.failed_tests == 0    


def test_tcp_test():
  smolder.tcp_test('127.0.0.1', 22)  # Are you running an ssh server?


def test_fail_tcp_test():
  assert_raises(Exception, smolder.tcp_test, '127.0.0.1', 4242)
