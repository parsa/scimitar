# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from . import local_session as _local, remote_session as _remote, offline_session as _offline
from utils import config
from sys import _getframe as ctx
import pexpect.pxssh as sp
import utils

_sessions = []

class UnknownCommandException(Exception):
    """Raised when the command called does not exist."""

    def __init__(self, cmd):
        self.message = 'Unknown command entered'
        self.expression = cmd

class BadArgsException(Exception):
    """Raised when arguments of a command are nonsense."""
    def __init__(self, cmd, expectation):
        self.message = expectation
        self.expression = cmd

class CommandFailedException(Exception):
    """Raised when command fails and no clue what's wrong."""
    def __init__(self, cmd, expectation):
        self.message = expectation
        self.expression = cmd

class BadConfigException(Exception):
    """Raised when configuration seems to have wrong values."""
    def __init__(self, cmd, expectation):
        self.message = expectation
        self.expression = cmd

class TimeOutException(Exception):
    """Can be raised when something times out."""
    pass

class CommandImplementationIncomplete(Exception):
    """Raised when a command I had to remove is called."""
    pass

# FIXME: Disabled for now
# MERGE: local_session (8c110db273af4a81bea68ef8686f1beb)
def start_local(pids):
    """Not active in this version"""
    raise CommandImplementationIncomplete
    #for pid in pids:
    #    new_session = _local.LocalSession(pid)
    #_sessions.append(new_session)

# FIXME: Changed this to assume one locality per node.
# MERGE: hpx_pids (4c2e6efda9334f50a97498ff3df4ca37)
# TODO: This function's too long. It needs to be refactored.
def node_ls(host_config, jobid):
    node_ls_result = None
    app_name = None
    try:
        # SSH to the head node.
        with sp.pxssh(echo=False) as conn:
            conn.login(host_config['hostname'], host_config['user'], original_prompt=host_config['PS1'])

            def send(x):
                conn.sendline(x)
                conn.prompt
                return conn.before

            # Get list of nodes.
            node_ls_cmd = host_config['node_ls'].format(jobid=jobid)
            node_ls_result = send(node_ls_cmd)
            print('\rnode_ls_result', node_ls_result)
            # Check if the listing command was successful.
            node_ls_status = send('echo $?')
            try:
                print('\rnode_ls_status', node_ls_status)
                if int(node_ls_status) != 0:
                    raise CommandFailedException('node_ls', 'Listing command failed with status code {}'.format(node_ls_status))
            except ValueError:
                raise CommandFailedException('node_ls', 'Listing command did not return a meaningful value')

            app_name_cmd = host_config['app_name']
            app_name = send(app_name_cmd)
            conn.logout()
    # Broken pipe
    except sp.ExceptionPxssh as e:
        raise CommandFailedException('node_ls', e.expectation)
    # Process the result and get the hostnames
    # TODO: Handle potential exceptions when the text was messed up.
    # TODO: Handle potential exceptions when the function messes up.
    nodes = host_config['node_ls_fn'](node_ls_result)
    if type(nodes) is not list:
        raise CommandFailedException('node_ls', 'Processing function did not return a list')
    return (nodes, app_name)

def find_pids(host_config, nodes, app_name):
    pids = {}
    for node in nodes:
        pid_ls_result = None
        try:
            # SSH to the head node.
            with sp.pxssh(echo=False) as conn:
                conn.login(host_config['hostname'], host_config['user'], original_prompt=host_config['PS1'])
                # Get list of nodes.
                pid_ls_cmd = host_config['pid_ls'].format(appname=app_name, jobid=jobid)

                def send(x):
                    conn.sendline(x)
                    conn.prompt
                    return conn.before

                pid_ls_result = send(node_ls_cmd)
                # Check if the listing command was successful.
                node_ls_status = send('echo $?')
                try:
                    if int(node_ls_status) != 0:
                        raise CommandFailedException('find_pids', 'Listing command failed with status code {}'.format(node_ls_status))
                except ValueError:
                    raise CommandFailedException('find_pids', 'Listing command did not return a meaningful value')

                conn.logout()
        # Broken pipe
        except sp.ExceptionPxssh as e:
            raise CommandFailedException('find_pids', e.expectation)
        sub_pids = host_config['pid_ls_fn'](pid_ls_result)
        if type(sub_pids) is not list:
            raise CommandFailedException('find_pids', 'Processing function did not return a list')
        pids[node] = sub_pids
    return pids

def start_remote(host, jobid):
    """Starts an SSH connection, finds all computing nodes in the batch job and
    connects to each to find the PIDs belonging to the HPX application.
    NOTE: Only PBS is supported at this point"""
    # Check if host is configured
    # NOTE: We're assuming host configurations are all in utils/config.py.
    if not host in config.remotes:
        raise BadArgsException('remote', 'Hostname not found in "utils/config.py"')
    # Get host configuration
    host_config = config.remotes[host]

    # List all nodes
    (nodes, app_name) = node_ls(host_config, jobid)
    print(app_name, nodes)

    # List all PIDs
    pids = find_pids(host, nodes, app_name)
    print(pids)

    #connect_all()
