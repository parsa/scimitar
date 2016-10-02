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
import sys
import hpx_threads as threads
from hpx.printers import *


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
    #pp = gdb.printing.RegexpCollectionPrettyPrinter('hpx')
    pp = printing.HPXPrinterCollection('hpx')

    for k, v in printer_dict.iteritems():
        pattern = '^%s$' % k
        pp.add_printer(k, pattern, v)

    return pp

def register_pretty_printer(obj):
    #gdb.printing.register_pretty_printer(
    printing.register_pretty_printer(
        obj, build_pretty_printers()
    )


class ReloadCommand(gdb.Command):

    def __init__(self):
        super(ReloadCommand, self).__init__("reload", gdb_cmd_type)

    def invoke(self, arg, from_tty):
        if arg and arg.strip():
            if sys.modules.has_key(arg):
                arg_mode = sys.modules[arg]
                reload(arg_mode)
                print('Module "%s" reloaded.\n' % arg)
            else:
                try:
                    print(
                        'Warning: "%s" was not previously loaded.\n' % arg
                    )
                    am = __import__(arg)
                    globals()[arg] = am
                    print('Module "%s" loaded.\n' % arg)
                except ImportError:
                    sys.stderr.write(
                        'Error: Failed to load "%s".\n' % arg
                    )
                    sys.stderr.flush()
        else:
            sys.stderr.write('No module name provided.\n')
            sys.stderr.flush()


gdb_cmd_type = gdb.COMMAND_NONE
if 'COMMAND_USER' in dir(gdb):
    gdb_cmd_type = gdb.COMMAND_USER
    
ReloadCommand()

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
