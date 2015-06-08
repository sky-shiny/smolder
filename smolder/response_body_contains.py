from yapsy.IPlugin import IPlugin
import logging
LOG = logging.getLogger('smolder')

class ResponseBodyContains(IPlugin):

    def run(self, req):
        # Did we expect something specific in the response body?
        required_text = req.test['outcomes']['response_body_contains']
        try:
            req_content = req.req.content.decode()
        except UnicodeDecodeError:
            req_content = req.req.content
        LOG.debug("Content: {0}".format(req_content))
        if required_text not in req_content:
            return req.fail_test("Body does not contain \"{0}\"".format(required_text))
        else:
            return req.pass_test("Body contains \"{0}\"".format(required_text))
