#!/usr/bin/env python
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

