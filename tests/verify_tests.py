#!/usr/bin/env python
import os
import logging
from charcoal import get_verify

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
LOG = logging.getLogger('smolder')
LOG.setLevel(logging.DEBUG)


def test_verify():
    assert (get_verify(True, 'https') == (True, True))
    assert (get_verify(True, 'http') == (True, True))
    assert (get_verify(True, 'tcp') == (True, True))
    assert (get_verify(True, None) == (True, True))
    assert (get_verify(False, 'https') == (False, True))
    assert (get_verify(False, 'http') == (False, True))
    assert (get_verify(False, 'tcp') == (False, True))
    assert (get_verify(False, None) == (False, True))
    assert (get_verify('True', 'tcp') == (True, True))
    assert (get_verify('False', 'tcp') == (False, True))
    assert (get_verify('True', 'http') == (True, True))
    assert (get_verify('False', 'http') == (False, True))
    assert (get_verify('True', 'https') == (True, True))
    assert (get_verify('False', 'https') == (False, True))
    assert (get_verify('True', None) == (True, True))
    assert (get_verify('False', None) == (False, True))
    assert (get_verify(None, 'https') == (True, False))
    assert (get_verify(None, 'http') == (False, False))
    assert (get_verify(None, 'tcp') == (False, False))
