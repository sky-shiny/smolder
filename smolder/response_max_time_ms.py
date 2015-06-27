from yapsy.IPlugin import IPlugin
import logging
LOG = logging.getLogger('smolder')


class ResponseMaxTimeMs(IPlugin):

    @staticmethod
    def run(req):

        # Check response time
        if req.duration_ms > int(req.test['outcomes']['response_max_time_ms']):
            longer_by_ms = req.duration_ms - int(req.test['outcomes']['response_max_time_ms'])
            return req.fail_test('Response time was {0}ms longer than {1}ms max ({2}ms)'.format(str(longer_by_ms), req.test['outcomes']['response_max_time_ms'], str(req.duration_ms)))
        else:
            shorter_by_ms = int(req.test['outcomes']['response_max_time_ms']) - req.duration_ms
            return req.pass_test('Response time was {0}ms shorter than max ({1}ms)'.format(str(shorter_by_ms), str(req.duration_ms)))
