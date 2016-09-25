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

def build_pretty_printers():
    printer_dict = {}

    include_dicts = lambda m: printer_dict.update(m.printer_dict)

    import backtrace, client_base, future, gid_type, thread_description, thread_state, tuple_

    include_dicts(backtrace)
    include_dicts(client_base)
    include_dicts(future)
    include_dicts(gid_type)
    include_dicts(thread_description)
    include_dicts(thread_state)
    include_dicts(tuple_)

    pp = gdb.printing.RegexpCollectionPrettyPrinter("hpx")

    for k, v in printer_dict.iteritems():

        pattern = '^%s$' % k
        pp.add_printer(k, pattern, v)

    return pp

