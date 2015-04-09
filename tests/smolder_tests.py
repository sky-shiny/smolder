#!/usr/bin/env python2
import smolder
import nose
from nose.tools import assert_raises

def test_noop():
  assert smolder.noop_test() == True

def test_tcp():
  smolder.tcp_test('127.0.0.1', 22) #Are you running an ssh server?

def test_tcp_fails():
  assert_raises(Exception, smolder.tcp_test, '127.0.0.1', 4242)
