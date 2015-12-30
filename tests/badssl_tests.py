# !/usr/bin/env python

from charcoal import Charcoal
import yaml
import os
import logging

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
LOG = logging.getLogger('smolder')
LOG.setLevel(logging.DEBUG)


def test_ssl_protocol():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='http://http.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0


def test_ssl_expired_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test, host='expired.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0


def test_ssl_wrong_host_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='wrong.host.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0


def test_ssl_self_signed_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='self-signed.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0


def test_ssl_sha1_2016_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='sha1-2016.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_sha1_2017_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='sha1-2017.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_sha256_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='sha256.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_1000_sans_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='1000-sans.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_10000_sans_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='10000-sans.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0


def test_ssl_incomplete_chain_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='incomplete-chain.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0


def test_ssl_rsa8192_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='rsa8192.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_mixed_script_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='mixed-script.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_very_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='very.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_mixed_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='mixed.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_mixed_favicon_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='mixed-favicon.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_cbc_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='cbc.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_rc4_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='rc4.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0


def test_ssl_mozilla_old_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='mozilla-old.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_mozilla_intermediate_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='mozilla-intermediate.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_mozilla_modern_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='mozilla-modern.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_dh480_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='dh480.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_dh1024_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='dh1024.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_dh2048_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='dh2048.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_dh_small_subgroup_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='dh-small-subgroup.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_dh_composite_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='dh-composite.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_hsts_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='hsts.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_upgrade_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='upgrade.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_preloaded_hsts_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='preloaded-hsts.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_subdomain_preloaded_hsts_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='subdomain.preloaded-hsts.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0


def test_ssl_http_password_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='http-password.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0


def test_ssl_pinning_test_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='pinning-test.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests == 0


def test_ssl_superfish_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='superfish.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0


def test_ssl_edellroot_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='edellroot.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0


def test_ssl_dsdtestprovider_badssl_com():
    total_failed_tests = 0
    total_passed_tests = 0
    myfile = open(THIS_DIR + '/fixtures/badssl.yaml')
    test_json = yaml.load(myfile)
    for test in test_json['tests']:
        test_obj = Charcoal(test=test,
                            host='dsdtestprovider.badssl.com')
        total_failed_tests += test_obj.failed
        total_passed_tests += test_obj.passed
    LOG.debug(total_failed_tests)
    assert total_failed_tests > 0
