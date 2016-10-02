#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from sys import modules

def __print_error__(msg):
    gdb.write(msg, gdb.STDERR)
    gdb.flush(gdb.STDERR)

try:
    if not modules.has_key('hpx'):
        import hpx
    else:
        reload(hpx)

    # Pretty Printers
    hpx.register_pretty_printer(gdb.current_objfile())

    # HPX Threads
    try:
        # If hpx_threads variable is available then the placeholder's there not
        # the actual module
        hpx.threads.hpx_threads_available
        __print_error__(
            'HPX Threading helper cannot be loaded. Please run hpx_threads.py '
            'to download the script from HPX\'s repository.\n'
        )
    except NameError:
        for cmd in [
            'define hook-continue',
            'hpx thread restore',
            'end',
        ]:
            gdb.execute(cmd)
except ImportError:
    __print_error__(
        'Unable to import hpx.\n'
        'Make sure the hpx-gdb directory is accessible to Python via sys.path '
        '(python sys.path.append("<Path to HPX hpx-gdb/python subdirectory>"))',
    )

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
