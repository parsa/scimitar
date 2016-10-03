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

commands = []
pretty_printers = {}

import gdb
import sys
import helpers.commands
import threads.commands
from hpx.printers import *

GDB_CMD_TYPE = gdb.COMMAND_NONE if 'COMMAND_USER' in dir(
    gdb
) else gdb.COMMAND_USER


def build_pretty_printers():
    # Introduce the types to GDB
    pcol = printing.RegexPrettyPrinterCollection('hpx')

    for k, v in pretty_printers.iteritems():
        pcol.add_printer(k, '^%s$' % k, v)

    return pcol


def register_pretty_printer(obj):
    printing.register_pretty_printer(obj, build_pretty_printers())



def register_commands():
    build_commands_list()
    for cmd in commands:
        cmd()


register_commands()

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
