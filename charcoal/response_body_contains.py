from yapsy.IPlugin import IPlugin
import logging
LOG = logging.getLogger('smolder')


class ResponseBodyContains(IPlugin):

    @staticmethod
    def run(req):
        # Did we expect something specific in the response body?
        required_text = req.test['outcomes']['response_body_contains']
        LOG.debug(required_text)
        try:
            req_content = req.req.content.decode()
        except UnicodeDecodeError:
            req_content = req.req.content
        LOG.debug("Content: {0}".format(req_content))
        if required_text not in req_content:
            return req.fail_test("\"{0}\" does not contain \"{1}\"".format(req_content, required_text))
        else:
            return req.pass_test("Body contains \"{0}\"".format(required_text))
