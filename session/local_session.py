# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from .exceptions import *
from . import modes
from util import configuration, print_ahead
import pexpect as sp
#############################
# mode: local
#############################
def raw(args):
    raise CommandImplementationIncompleteError

def attach(args):
    raise CommandImplementationIncompleteError

def ask(args):
    raise CommandImplementationIncompleteError

commands = {
    'raw': raw,
    'attach': attach,
    'ask': ask,
    'quit': quit,
}

def process(cmd, args):
    raise CommandImplementationIncompleteError
    #return (modes.local, None)

# FIXME: Disabled for now
# MERGE: local_session (8c110db273af4a81bea68ef8686f1beb)
def launch(pids):
    """Not active in this version"""
    raise CommandImplementationIncompleteError
    #for pid in pids:
    #    new_session = _local.LocalSession(pid)
    #_sessions.append(new_session)

def quit(args):
    raise CommandImplementationIncompleteError

class LocalSession():
    def __init__(self, PIDs):
        self.pids=PIDs
        raise CommandImplementationIncompleteError

    def query(self):
        raise CommandImplementationIncompleteError

    def __enter__(self):
        raise CommandImplementationIncompleteError

    def __exit__(self):
        raise CommandImplementationIncompleteError

