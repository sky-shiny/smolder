from yapsy.IPlugin import IPlugin
import logging
import re
LOG = logging.getLogger('smolder')


class ResponseHeaderValueContains(IPlugin):

    @staticmethod
    def run(req):

        for header in req.test['outcomes']['response_header_value_contains']:
            if header not in req.req.headers:
                return req.fail_test("Expected header {0} not present".format(header))
            elif not re.search(req.test['outcomes']['response_header_value_contains'][header], req.req.headers[header]):
                return req.fail_test("Expecting {0}: {1}, got {2}: {3}".format(
                    header,
                    req.test['outcomes']['response_header_value_contains'][header],
                    header,
                    req.req.headers[header]))
            else:
                return req.pass_test("Header {0}: {1} present".format(header, req.req.headers[header]))
