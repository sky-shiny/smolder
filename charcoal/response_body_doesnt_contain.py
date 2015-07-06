from yapsy.IPlugin import IPlugin
import logging
LOG = logging.getLogger('smolder')


class ResponseBodyDoesntContain(IPlugin):

    @staticmethod
    def run(req):

        # Do we need to ensure something does NOT appear in the response body?
        banned_text = req.test['outcomes']['response_body_doesnt_contain']
        try:
            req_content = req.req.content.decode()
        except UnicodeDecodeError:
            req_content = req.req.content
        if banned_text in req_content:
            return req.fail_test("Body contains \"{0}\" and shouldn't".format(banned_text))
        else:
            return req.pass_test("Body doesn't contain \"{0}\"".format(banned_text))
