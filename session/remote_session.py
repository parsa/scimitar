# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from .exceptions import *
from . import modes
from utils import config
import pexpect.pxssh as sp
##############################
# mode: remote
##############################

# FIXME: RemoteSession should live in a different thread. Whenever connection
# dies or is closed session mode should change instantly. Exceptions must be
# handled properly, too

# TODO: If response didn't come by after a certain timeout passes return pending
def process(cmd, args):
    """Sends a query and retrieves the response"""
    session = globals()['session']
    response = None
    line = cmd + ' '.join(args)
    try:
        response = session.query(line)
    # FIXME: Find out what exceptions will be passed and handle them properly
    except Exception as e:
        pass
    return (modes.remote, response)

def launch(host, jobid):
    session = RemoteSession(host, jobid)
    globals()['session'] = session
    #session.disconnect_all()

class RemoteSession():
    def __init__(self, host, jobid):
        """Starts an SSH connection, finds all computing nodes in the batch job
        and connects to each to find the PIDs belonging to the HPX application.
        NOTE: Only PBS is supported at this point"""
        # Check if host is configured
        # NOTE: We're assuming host configurations are all in utils/config.py.
        if not host in config.remotes:
            raise BadArgsException('remote', 'Hostname not found in "utils/config.py"')
        # Scheduler Job ID
        self.jobid = jobid
        # Get configuration
        self.host_config = config.remotes[host]
        self.app_name, self.nodes, self.job = None, None, {}
        # Find application name, nodes, PIDs
        self.examine_job()

        self.remote_terminals = []
        self.active_terminal = None
        self.connect_all()

    def query(self, line):
        self.active_terminal.sendline(line)
        self.active_terminal.prompt()
        return str(self.active_terminal.before, 'ascii')

    # FIXME: Changed this to assume one locality per node.
    # MERGE: hpx_pids (4c2e6efda9334f50a97498ff3df4ca37)
    # TODO: This function's too long. It needs to be refactored.
    def examine_job(self):
        '''Attempts to retrieve job information. Returns a tuple of a)
        application name, b) list of nodes, and c) a dictionary of PIDs'''
        try:
            # SSH to the head node.
            with sp.pxssh(echo=False) as conn:
                cfg = self.host_config['hostname'], self.host_config['user'], self.host_config['PS1']
                conn.login(cfg[0], cfg[1], original_prompt=cfg[2])

                # Shorthand for easily sending commands
                def send(x):
                    conn.sendline(x)
                    conn.prompt()
                    return str(conn.before, 'ascii')

                # Get list of nodes.
                node_ls_cmd = self.host_config['node_ls'].format(jobid=self.jobid)
                node_ls_result = send(node_ls_cmd)
                # Check if the listing command was successful.
                node_ls_status = send('echo $?')
                try:
                    node_ls_status = int(node_ls_status)
                    if node_ls_status != 0:
                        raise CommandFailedException('examine_job', 'Listing failed with status code {0}. Job ID {1} may be incorrect'.format(node_ls_status, self.jobid))
                except ValueError:
                    raise CommandFailedException('examine_job', 'Got an unexpected result from the listing command. Command cannot proceed')

                # Process the result and get the hostnames
                # TODO: Handle potential exceptions when the text was messed up.
                # TODO: Handle potential exceptions when the function messes up.
                self.nodes = self.host_config['node_ls_fn'](node_ls_result)
                if type(self.nodes) is not list:
                    raise CommandFailedException('examine_job', 'Processing function did not return a list')

                # TODO: Check if it actually returned a name
                # Retrieve application name
                app_name_cmd = self.host_config['app_name'].format(host=self.nodes[0])
                app_name_fn = self.host_config['app_name_fn']
                app_name_raw = send(app_name_cmd)
                if not app_name_raw:
                    raise CommandFailedException('examine_job', 'No running MPI application found')
                self.app_name = app_name_fn(app_name_raw)
                # app_name probably is path so it won't work with commands like psgrep
                app_short_name = self.app_name.split('/')[-1]

                # Connect and collect PIDs
                for node in self.nodes:
                    # TODO: Check if it actually returned PIDs
                    # Build the command
                    pid_ls_cmd = self.host_config['pid_ls'].format(host=node, appname=app_short_name)
                    # Send the command
                    pids_raw = send(pid_ls_cmd)
                    # Process the list
                    pid_ls_fn = self.host_config['pid_ls_fn']
                    pids = pid_ls_fn(pids_raw)
                    # See if it actually is a list or not
                    if type(pids) is not list:
                        raise CommandFailedException('find_pids', 'Processing function did not return a list')
                    # Add to the dictionary
                    self.job[node] = pids

                conn.logout()
        # Broken pipe
        except sp.ExceptionPxssh as e:
            raise CommandFailedException('examine_job', e.expectation)

    def connect_all(self):
        gdb_config = config.settings['gdb']
        gdb_cmd = gdb_config['cmd']

        for node, pids in self.job.items():
            for pid in pids:
                try:
                    print('+++Connecting+++')
                    conn = sp.pxssh(echo=False)
                    print(self.host_config['hostname'], self.host_config['user'], self.host_config['PS1'])
                    conn.login(self.host_config['hostname'], self.host_config['user'], self.host_config['PS1'])
                    print(conn.before)
                    print(conn.after)

                    # Build the command line and launch GDB
                    cmd = ['ssh', node]
                    gdb_cmd.append(gdb_config['attach'].format(pid=pid))
                    cmd.extend(gdb_cmd)

                    gdb_str = ' '.join(cmd)
                    print('gdb_str:', gdb_str)
                    conn.sendline(gdb_str)
                    conn.prompt(120)
                    conn.sync_original_prompt()
                    print(conn.after)
                    print(conn.before)

                    print('+++Connected+++')

                    self.remote_terminals.append(conn)

                except sp.ExceptionPxssh as e:
                    raise e

        self.active_terminal = self.remote_terminals[0]

    def disconnect_all(remote_terms):
        self.active_terminal = None
        for term in self.remote_terminals:
            term.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.disconnect_all()

