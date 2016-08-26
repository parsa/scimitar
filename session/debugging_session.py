'''
    Scimitar: Ye Distributed Debugger
    ~~~~~~~~
    :copyright:
    Copyright (c) 2016 Parsa Amini
    Copyright (c) 2016 Hartmut Kaiser
    Copyright (c) 2016 Thomas Heller

    :license:
    Distributed under the Boost Software License, Version 1.0. (See accompanying
    file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
'''

from . import modes, local_session as _local_s, remote_session as _remote_s
from .exceptions import *
from util import config, print_ahead
#######################
# mode: debugging
#######################
def process(pids):
    raise CommandImplementationIncompleteError

def quit(args):
    raise CommandImplementationIncompleteError

