#!/usr/bin/env python
def get_verify(verify=None, protocol=None):
    """

    :rtype: (bool, bool)
    :return: Should we verify the ssl request and did the user request that we do so.
    :param verify: bool | str
        The argument to pass through to requests to verify SSL.
    :param protocol: str
        Default protocol is https.  Is used to provide defaults for verify.
    """
    if verify is not None:
        if type(verify) == bool:
            intermediate_verify = verify
        elif verify == "True":
            intermediate_verify = True
        elif verify == "False":
            intermediate_verify = False
        elif type(verify) == str:
            intermediate_verify = verify
        else:
            raise TypeError('Should never happen')
        return intermediate_verify, True
    else:
        if 'https' in protocol:
            return True, False
        else:
            return False, False
