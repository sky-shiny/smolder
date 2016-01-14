# -*- coding: utf-8 -*-

"""
Smolder Smoke Testing Library and cli

:copyright: (c) 2015 by Maxwell Cameron.
:license: BSD 3, see LICENSE for more details.

"""

__title__ = 'smolder'
# __version__ = '0.0.1'
# __build__ = 0x020501
__author__ = 'Max Cameron'
__license__ = 'BSD License'
__copyright__ = 'Copyright 2015 Maxwell Cameron'

from .tcptest import tcp_test
from .colours import Colours
from .colours import COLOURS
from .charcoal import Charcoal
from .get_verify import get_verify
from .get_host_overrides import get_host_overrides
from .output import Output

__all__ = ['.']
