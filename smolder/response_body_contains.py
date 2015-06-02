from yapsy.IPlugin import IPlugin
import smolder
import logging
LOG = logging.getLogger('smolder')

class ExpectStatusCode(IPlugin):

    def run(self, req):
        # Did we expect something specific in the response body?
        required_text = req.test['outcomes']['response_body_contains']
        try:
            req_content = req.req.content.decode()
        except UnicodeDecodeError:
            req_content = req.req.content
        if required_text not in req_content:
            return req.fail_test("Body contains \"{0}\"".format(required_text))
        else:
            return req.pass_test("Body contains \"{0}\"".format(required_text))
