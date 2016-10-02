# coding: utf-8

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
import gdb
import gdb.printing
import hpx_threads as threads
from hpx.printers import *
import imp
import sys


def build_pretty_printers():
    printer_dict = {}
    # Shorthand for adding a dictionary to printer_dict
    inc_dict = lambda m: printer_dict.update(m.printer_dict)
    # Combine all dictionaries
    inc_dict(backtrace)
    inc_dict(client_base)
    inc_dict(future)
    inc_dict(gid_type)
    inc_dict(thread_description)
    inc_dict(thread_state)
    inc_dict(tuple_)

    # Introduce the types to GDB
    pp = gdb.printing.RegexpCollectionPrettyPrinter("hpx")

    for k, v in printer_dict.iteritems():
        pattern = '^%s$' % k
        pp.add_printer(k, pattern, v)

    return pp


class ReloadCommand(gdb.Command):

    def __init__(self):
        super(ReloadCommand, self).__init__("reload", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        if arg and arg.strip():
            if sys.modules.has_key(arg):
                arg_mode = sys.modules[arg]
                reload(arg_mode)
                gdb.write('Module "%s" reloaded.\n' % arg)
            else:
                try:
                    gdb.write(
                        'Warning: "%s" was not previously loaded.\n' % arg,
                        gdb.STDOUT
                    )
                    am = __import__(arg)
                    globals()[arg] = am
                    gdb.write('Module "%s" loaded.\n' % arg)
                except ImportError:
                    gdb.write(
                        'Error: Failed to load "%s".\n' % arg, gdb.STDERR
                    )
        else:
            gdb.write('No module name provided.\n', gdb.STDERR)


ReloadCommand()

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
