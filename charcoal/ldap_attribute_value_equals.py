from yapsy.IPlugin import IPlugin

import logging
LOG = logging.getLogger('smolder')

class LdapAttributeValueEquals(IPlugin):

    @staticmethod
    def run(req):

        connection = req.req
        match = connection.compare(dn=req.test['inputs']['dn'], attribute=req.test['inputs']['attr_key'], value=req.test['outcomes']['ldap_attribute_value_equals'])

        if match:
             return req.pass_test("%s,%s=%s" % (req.test['inputs']['attr_key'], req.test['inputs']['dn'], req.test['outcomes']['ldap_attribute_value_equals']))

        else:
            connection.search(search_base=req.test['inputs']['dn'], attributes=req.test['inputs']['attr_key'], search_filter="(" + req.test['inputs']['attr_key'] + "=*)")
           
            actual_value = connection.response[0]['attributes'][req.test['inputs']['attr_key']]
            return req.fail_test("%s,%s != '%s' (Got '%s' instead)" % (req.test['inputs']['attr_key'], req.test['inputs']['dn'], req.test['outcomes']['ldap_attribute_value_equals'], actual_value))
