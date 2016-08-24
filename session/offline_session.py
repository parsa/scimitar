# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from . import modes, local_session as _local_s, remote_session as _remote_s
from .exceptions import *
from utils import config
#######################
# mode: offline
#######################
# Valid commands:
## local <pid>[ <pid>...]
## remote <login_node_hostname> <app_name> <jobid>
## quit
def local(args):
    try:
        pids = []
        for arg in args:
            pids.append(int(arg))
        _local_s.start_local(pids)
        return (modes.to_local, None)
    except TypeError:
        return (modes.offline, 'Was expecting PIDs, received a non-integer')
    _local_s.launch(pids)
    raise CommandImplementationIncomplete
    #return (modes.offline, None)
    
def remote(args):
    if len(args) != 2:
        raise BadArgsException('remote', 'remote <login_node_hostname> <jobid>')
    _remote_s.launch(host=args[0], jobid=args[1])
    return (modes.remote, None)
    
def quit(args):
    return (modes.quit, None)

commands = {
    'local': local,
    'remote': remote,
    'quit': quit,
}

def process(cmd, args):
    if cmd in commands:
        return commands[cmd](args)
    raise UnknownCommandException(cmd)

