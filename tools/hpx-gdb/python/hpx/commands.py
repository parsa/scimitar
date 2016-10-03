# coding: utf-8
#
# Scimitar: Ye Distributed Debugger
# 
# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#
import gdb
import sys
import hpx


class ReloadCommand(gdb.Command):

    def __init__(self):
        super(ReloadCommand, self).__init__("reload", hpx.GDB_CMD_TYPE)

    def invoke(self, arg, from_tty):
        if arg and arg.strip():
            if sys.modules.has_key(arg):
                arg_mode = sys.modules[arg]
                reload(arg_mode)
                sys.stdout.write('Module "%s" reloaded.\n' % arg)
            else:
                try:
                    sys.stdout.write(
                        'Warning: "%s" was not previously loaded.\n' % arg
                    )
                    am = __import__(arg)
                    sys.stdout.write('Module "%s" loaded.\n' % arg)
                except ImportError:
                    sys.stderr.write('Error: Failed to load "%s".\n' % arg)
                    sys.stderr.flush()
        else:
            sys.stderr.write('No module name provided.\n')
            sys.stderr.flush()


__commands__ = (ReloadCommand, )

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
