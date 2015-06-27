from yapsy.IPlugin import IPlugin
import logging
LOG = logging.getLogger('smolder')


class ResponseRedirect(IPlugin):

    @staticmethod
    def run(req):
        if req.test['outcomes']['response_redirect'] == req.req.headers['location']:
            message = req.pass_test("Redirect to {0}".format(req.test['outcomes']['response_redirect']))
            return message
        else:
            return req.fail_test("Got redirected to {0} instead of {1}".format(
                req.req.headers['location'],
                req.test['outcomes']['response_redirect']))
