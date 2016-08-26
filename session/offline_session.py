# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from . import modes, local_session as _local_s, remote_session as _remote_s
from .exceptions import *
from util import config, print_ahead
#######################
# mode: offline
#######################
# Valid commands:
## $ local raw
## $ local attach <pid>[ <pid>...]
## $ local ls
## $ local ls <regex_pattern>
## $ local do <routine>
## $ remote <machine_name> <jobid>
## $ remote <machine_name> ls
## $ remote <machine_name> attach <app_name> <node:pid>[ <node:pid>...]
## $ remote <machine_name> do <routine>
## quit
def local(args):
    try:
        pids = []
        for arg in args:
            pids.append(int(arg))
        _local_s.launch(pids)
        return (modes.to_local, None)
    except TypeError:
        raise BadArgsError('local', 'Was expecting PIDs, received a non-integer')
    _local_s.launch(pids)
    raise CommandImplementationIncompleteError
    #return (modes.local, None)
    
def remote(args):
    if len(args) != 2:
        raise BadArgsError('remote', 'remote <machine_name> <jobid>')
    #print_ahead('Launching remote session')
    _remote_s.launch(name=args[0], jobid=args[1])
    return (modes.remote, None)
    
def quit(args):
    return (modes.quit, None)

def debug(args):
    import pdb; pdb.set_trace()
    return (modes.offline, None)

commands = {
    'local': local,
    'remote': remote,
    'quit': quit,
    'debug': debug,
}

def process(cmd, args):
    if cmd in commands:
        return commands[cmd](args)
    raise UnknownCommandError(cmd)

