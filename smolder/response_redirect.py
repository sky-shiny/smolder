from yapsy.IPlugin import IPlugin
import smolder
import logging
LOG = logging.getLogger('smolder')

class ExpectStatusCode(IPlugin):

    def run(self, req):
        if int(req.test['outcomes']['expect_status_code']) == req.req.status_code and req.test['outcomes']['response_redirect'] == req.req.headers['location']:
            message = req.pass_test("Status code == {0} and redirect == {1}".format(req.test['outcomes']['expect_status_code'], req.test['outcomes']['response_redirect']))
            return message
        else:
            return req.fail_test("Got status code {0} but got redirected to {1} instead of {2}".format(
                req.test['outcomes']['expect_status_code'],
                req.req.headers['location'],
                req.test['outcomes']['response_redirect']))
