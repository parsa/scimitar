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
import re
import scimitar


class ScimitarGdbError(Exception):

    def __init__(self, cmd, expectation):
        self.message = expectation
        self.expression = cmd


class ScimitarGdbCommand(gdb.Command):

    def __init__(
        self, command_class, completer_class = gdb.COMPLETE_NONE, prefix = True
    ):
        gdb.Command.__init__(
            self, command_class, scimitar.GDB_CMD_TYPE, completer_class, prefix
        )

    #def invoke(self, arg, from_tty):
    #    raise ScimitarGdbCommand
    #
    #def dont_repeat(self):
    #    pass
    #
    #def complete(self, text, word):
    #    pass


class ScimitarPrettyPrinter(object):

    def __init__(self, value):
        self.value = value

    # vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
