#!/usr/bin/env python
import os
import logging
import charcoal.get_verify

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
LOG = logging.getLogger('smolder')
LOG.setLevel(logging.DEBUG)


def test_verify():
    assert (charcoal.get_verify(True, 'https') == (True, True))
    assert (charcoal.get_verify(True, 'http') == (True, True))
    assert (charcoal.get_verify(True, 'tcp') == (True, True))
    assert (charcoal.get_verify(True, None) == (True, True))
    assert (charcoal.get_verify(False, 'https') == (False, True))
    assert (charcoal.get_verify(False, 'http') == (False, True))
    assert (charcoal.get_verify(False, 'tcp') == (False, True))
    assert (charcoal.get_verify(False, None) == (False, True))
    assert (charcoal.get_verify('True', 'tcp') == (True, True))
    assert (charcoal.get_verify('False', 'tcp') == (False, True))
    assert (charcoal.get_verify('True', 'http') == (True, True))
    assert (charcoal.get_verify('False', 'http') == (False, True))
    assert (charcoal.get_verify('True', 'https') == (True, True))
    assert (charcoal.get_verify('False', 'https') == (False, True))
    assert (charcoal.get_verify('True', None) == (True, True))
    assert (charcoal.get_verify('False', None) == (False, True))
    assert (charcoal.get_verify(None, 'https') == (True, False))
    assert (charcoal.get_verify(None, 'http') == (False, False))
    assert (charcoal.get_verify(None, 'tcp') == (False, False))
