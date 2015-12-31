#!/usr/bin/env python
# coding: utf-8 -*-

# Quick and dirty Ansible module to smoke test info.
#
__author__ = 'maxcameron'

from ansible.module_utils.basic import *
import json

#
try:
    from smolder import Charcoal

    HAS_SMOLDER = True
except ImportError:
    HAS_SMOLDER = False

DOCUMENTATION = '''
---
module: smolder
short_description: Run a smolder test against a host
description:
   - Given a Smolder test as yaml a hostname or ip address, run the test against the host and process the results.
version_added: "1.9"
author: Max Cameron
requirements:
  - smolder
options:
  test:
    required: true
    description:
      - smolder test yaml
  host:
    required: true
    description:
      - ip address or hostname
  force:
    required: false
    description:
      - Boolean whether to allow non GET requests
'''

EXAMPLES = '''
  smolder: host=status.github.com
    name: "Github Status"
    outcomes:
      expect_status_code: 301
      response_redirect: "https://status.github.com/api/status.json"
    inputs:
      headers:
        User-Agent: "Smolder smoke test library"
    uri: /api/status.json
'''


def main():
    all_tests = []
    total_passed_tests = 0
    total_failed_tests = 0
    argument_spec = dict(
        host=dict(required=True),
        test=dict(required=True, type='dict')
    )

    module = AnsibleModule(argument_spec)
    test_input = module.params["test"]
    if not HAS_SMOLDER:
        module.fail_json(msg='smolder is required for this module')

    test_obj = Charcoal(test=test_input, host=module.params["host"], output_format='json')
    total_failed_tests += test_obj.failed
    total_passed_tests += test_obj.passed
    all_tests.append(test_obj)
    test_output = json.loads(str(test_obj))
    if total_failed_tests > 0:
        module.fail_json(msg="FOUND {0} FAILURES IN {1} TESTS".format(
            str(total_failed_tests), str(total_passed_tests + total_failed_tests)),
            stdout='\n\033[0m' + test_output['msg'])
    elif total_failed_tests == 0 and total_passed_tests == 0:
        module.fail_json(msg="No tests run: check plugins", stdout='\n\033[0m' + test_output['msg'])
    else:
        module.exit_json(msg="ALL TESTS PASSED!", stdout='\n\033[0m' +
                         test_output['msg'],
                         response_headers=test_output['response_headers'],
                         response_status_code=test_output['response_status_code'],
                         request_inputs=test_output['request_inputs'])


if __name__ == '__main__':
    main()
