# -*- coding: utf-8 -*-
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
import commands
import threads.commands
from hpx.printers import *

GDB_CMD_TYPE = gdb.COMMAND_NONE if 'COMMAND_USER' in dir(
    gdb
) else gdb.COMMAND_USER

__commands__ = []


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
    pp = printing.HPXPrinterCollection('hpx')

    for k, v in printer_dict.iteritems():
        pattern = '^%s$' % k
        pp.add_printer(k, pattern, v)

    return pp


def register_pretty_printer(obj):
    printing.register_pretty_printer(obj, build_pretty_printers())


def build_commands_list():
    __commands__.extend(commands.__commands__)
    __commands__.extend(threads.commands.__commands__)


def register_commands():
    build_commands_list()
    for cmd in __commands__:
        cmd()

register_commands()

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
