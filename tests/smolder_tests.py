#!/usr/bin/env python2
import smolder
import nose
import json
import os
from nose.tools import assert_raises
from imp import reload

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

def test_noop_test():
  assert smolder.noop_test()

def test_github_status():
  myfile = open(THIS_DIR + '/github_status.json')
  test_json = json.load(myfile)
  for test in test_json['tests']:
    smolder.http_test(test, 'status.github.com', False)
  reload(smolder)
  assert smolder.failed_tests == 0

def test_github_status_response_time_expect_fail():
  myfile = open(THIS_DIR + '/harsh_github_status.json')
  test_json = json.load(myfile)
  for test in test_json['tests']:
    test_obj = smolder.charcoal.Charcoal(test=test, host=kwargs['host'])
    smolder.http_test(test, 'status.github.com', False)
  reload(smolder)
  assert smolder.failed_tests > 0

def test_tcp_test():
  smolder.tcp_test('127.0.0.1', 22) #Are you running an ssh server?

def test_fail_tcp_test():
  assert_raises(Exception, smolder.tcp_test, '127.0.0.1', 4242)

