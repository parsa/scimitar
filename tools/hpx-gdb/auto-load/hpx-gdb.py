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

try:
    if not 'hpx' in dir():
        import hpx
    else:
        reload(hpx)
except ImportError:
    print(
        'Unable to import the printers module. '
        'Add the printers directory to sys.path '
        '(python sys.path.append("<Path to HPX hpx-gdb/python subdirectory>"))'
    )

gdb.printing.register_pretty_printer(
    gdb.current_objfile(),
    hpx.build_pretty_printers())

