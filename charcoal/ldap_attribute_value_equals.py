from yapsy.IPlugin import IPlugin
import ldap
import logging
LOG = logging.getLogger('smolder')

class LdapAttributeValueEquals(IPlugin):

    @staticmethod
    def run(req):

        try:
            match = req.req.compare_s(req.test['inputs']['dn'], req.test['inputs']['attr_key'], req.test['outcomes']['ldap_attribute_value_equals'])
        except ldap.LDAPError:
            return  req.fail_test("Couldn't query LDAP database using dn=%s to ensure that key '%s'='%s'" % (req.test['inputs']['dn'], req.test['inputs']['attr_key'], req.test['inputs']['attr_value']))
            
        if match == 1:
             return req.pass_test("%s,%s=%s" % (req.test['inputs']['attr_key'], req.test['inputs']['dn'], req.test['outcomes']['ldap_attribute_value_equals']))

        else:
            (_, data) = req.req.search_s(base=req.test['inputs']['dn'], scope=ldap.SCOPE_BASE, attrlist=[str(req.test['inputs']['attr_key'])])[0]
            actual_value = data[req.test['inputs']['attr_key']][0]
            return req.fail_test("%s,%s != '%s' (Got '%s' instead)" % (req.test['inputs']['attr_key'], req.test['inputs']['dn'], req.test['outcomes']['ldap_attribute_value_equals'], actual_value))
