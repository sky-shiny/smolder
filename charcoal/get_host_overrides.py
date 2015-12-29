#!/usr/bin/env python

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def get_host_overrides(host, port):
    """

    :param port:
    :type host: str
    :param host:
    """
    host_overrides_object = urlparse(host)
    host_overrides = dict()
    if host_overrides_object.scheme is not None and host_overrides_object.scheme is not "":
        host_overrides["protocol"] = host_overrides_object.scheme
    else:
        host_overrides["protocol"] = 'http'
    if host_overrides_object.port is not None:
        host_overrides["port"] = host_overrides_object.port
    else:
        host_overrides["port"] = port
    host_overrides['hostname'] = host_overrides_object.hostname
    return host_overrides
