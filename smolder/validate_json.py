from yapsy.IPlugin import IPlugin
import validictory


class ValidateJson(IPlugin):

    @staticmethod
    def run(req):
        try:
            validictory.validate(req.req.json(), req.test['outcomes']['schema'])
            return req.pass_test("Json response matches the schema provided")
        except ValueError as error:
            return req.fail_test("Json response fails to match the schema provided {0}".format(error))
