from yapsy.IPlugin import IPlugin
import dpath
import logging
LOG = logging.getLogger('smolder')


class ResponseJsonContains(IPlugin):

    @staticmethod
    def run(req):
        # Validate presence of partial dicts in response json
        for path in list(req.test['outcomes']['response_json_contains'].keys()):
            expected_value = req.test['outcomes']['response_json_contains'][path]
            actual_value = dpath.util.search(req.req.json(), path)[path]
            if expected_value == actual_value:
                return req.pass_test("Body contains expected json value at path \"{0}\"".format(path))
            else:
                return req.fail_test("Invalid json value {0} at path \"{1}\", expecting {2}".format(actual_value, path, expected_value))
