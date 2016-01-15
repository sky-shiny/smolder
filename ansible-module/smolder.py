#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2014, Max Cameron <max.cameron@gmail.com> github.com/mcameron
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
import json

__author__ = 'maxcameron'

try:
    from smolder import Charcoal

    HAS_SMOLDER = True
except ImportError:
    HAS_SMOLDER = False

DOCUMENTATION = '''
---
module: smolder
short_description: Run a smolder test against a host http://sky-shiny.github.io/smolder/
description:
   - Given a Smolder test as yaml and a hostname or ip address, run the test against the host and process the results.
version_added: "2.1"
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
'''

EXAMPLES = '''
  - name: Test github status
    smolder:
      host: status.github.com
      test:
        name: "Github Status"
        outcomes:
          expect_status_code: 301
          response_redirect: "https://status.github.com/api/status.json"
        inputs:
          headers:
            User-Agent: "Smolder smoke test library"
        uri: /api/status.json
  - name: Test github status ssl
    smolder:
      host: status.github.com
      test:
        inputs:
          headers:
            User-Agent: "Smolder smoke test library"
        name: "Github Status ssl"
        outcomes:
            response_json_contains:
                status: good
            response_max_time_ms: 200
        port: 443
        protocol: https
        uri: /api/status.json
  - name: Test connectivity API -> MDTP end to end
    smolder:
      host: api-definition.service
      test:
        tcp_test: True
        name: "Test connectivity API -> MDTP end to end"
        outcomes:
            expect_status_code: 200
            response_max_time_ms: 600
            response_json_contains:
                status: good
        inputs:
            verify: False
            headers:
                Accept: "application/vnd.hmrc.1.0+json"
                User-Agent: "Smolder smoke test library"
        uri: /api-definition
'''

RETURN = '''
response_headers:
  description: the response headers received
  returned: success
  type: string
response_status_code:
  description: the response status code
  returned: success
  type: string
'''


def main():
    argument_spec = dict(
        host=dict(required=True),
        test=dict(required=True, type='dict')
    )

    module = AnsibleModule(argument_spec)
    test_input = module.params["test"]
    if not HAS_SMOLDER:
        module.fail_json(msg='smolder is required for this module')

    test_obj = Charcoal(test=test_input, host=module.params["host"], output_format='json')
    test_output = json.loads(str(test_obj))
    if test_obj.failed > 0:
        module.fail_json(msg="FOUND {0} FAILURES IN {1} TESTS".format(
            str(test_obj.failed), str(test_obj.passed + test_obj.failed)),
            stdout='\n\033[0m' + test_output['msg'])
    elif test_obj.failed == 0 and test_obj.passed == 0:
        module.fail_json(msg="No tests run: check plugins", stdout='\n\033[0m' + test_output['msg'])
    else:
        module.exit_json(msg="ALL TESTS PASSED!", stdout='\n\033[0m' +
                         test_output['msg'],
                         response_headers=test_output['response_headers'],
                         response_status_code=test_output['response_status_code'],
                         request_inputs=test_output['request_inputs'])

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
