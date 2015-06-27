from yapsy.IPlugin import IPlugin
import logging
LOG = logging.getLogger('smolder')


class HeadersPresent(IPlugin):

    @staticmethod
    def run(req):
        for header in req.test['response_headers_present']:
            if header not in req.req.headers:
                return req.fail_test("Expected header {0} not present".format(header))
            else:
                return req.pass_test("Header {0}: {1} present".format(header, req.req.headers[header]))
