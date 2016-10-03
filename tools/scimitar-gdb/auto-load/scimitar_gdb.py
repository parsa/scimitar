#!/usr/bin/env python
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


def __print_error__(msg):
    sys.stderr.write(msg)
    sys.stderr.flush()


try:
    import scimitar

    # Pretty Printers
    scimitar.register_pretty_printer(gdb.current_objfile())

except ImportError:
    __print_error__(
        'Unable to import scimitar.\n'
        'Make sure the scimitar-gdb directory is accessible to Python via sys.path\n'
    )

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
