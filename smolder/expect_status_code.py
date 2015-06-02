
from yapsy.IPlugin import IPlugin
import smolder
import logging
LOG = logging.getLogger('smolder')
LOG.info("Hello")

class ExpectStatusCode(IPlugin):

    def run(self, req):
        if 'expect_status_code' in req.test['outcomes']:
            if int(req.test['outcomes']['expect_status_code']) == req.req.status_code:
                return req.pass_test("Status code == {0}".format(req.test['outcomes']['expect_status_code']))
            else:
                return req.fail_test("Expecting status code {0} but got {1} instead".format(req.test['outcomes']['expect_status_code'], str(req.req.status_code)))
        else:
            if req.req.status_code == 200:
                return req.pass_test("Status code == 200")
            else:
                return req.fail_test("Status code != 200: {0}".format(req.req.status_code))
