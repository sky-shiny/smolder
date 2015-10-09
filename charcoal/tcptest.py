#!/usr/bin/env python
import logging
import socket
from retrying import retry
from .colours import COLOURS


FORMAT = '%(asctime)-15s %(name)s [%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.ERROR, datefmt="%Y-%m-%d %H:%M:%S")
LOG = logging.getLogger('smolder')


@retry(wait_exponential_multiplier=500, wait_exponential_max=30000, stop_max_attempt_number=7)
def tcp_test(host, port):
    """
    Attempts to make a TCP socket connection on the specified host and
    port. Returns true if successful. Else returns false.

    """
    LOG.debug("TCP test called")
    my_sock = None
    try:
        my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_sock.settimeout(1)
        my_sock.connect((host, port))
        print("Connecting to {0} on port {1} {2}".format(host, port, COLOURS.to_green("[PASS]")))
        my_sock.shutdown(2)
        my_sock.close()
    except socket.error:
        my_sock.close()
        print("Connecting to {0} on port {1} {2}".format(host, port, COLOURS.to_yellow("[FAIL]")))
        LOG.debug("Waiting for {0}:{1} to accept a connection".format(host, port))
        raise
    except Exception as error:
        print("Connecting to {0} on port {1} {2}".format(host, port, COLOURS.to_yellow("[FAIL]")))
        LOG.debug("TCP test failed: {0}".format(error))
        raise
