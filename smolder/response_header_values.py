from yapsy.IPlugin import IPlugin
import logging
LOG = logging.getLogger('smolder')


class ResponseHeaderValues(IPlugin):

    @staticmethod
    def run(req):

        for header in req.test['outcomes']['response_header_values']:
            if header not in req.req.headers:
                return req.fail_test("Expected header {0} not present".format(header))
            elif req.req.headers[header] != req.test['outcomes']['response_header_values'][header]:
                return req.fail_test("Expecting {0}: {1}, got {2}: {3}".format(
                    header,
                    req.test['outcomes']['response_header_values'][header],
                    header,
                    req.req.headers[header]))
            else:
                return req.pass_test("Header {0}: {1} present".format(header, req.req.headers[header]))
