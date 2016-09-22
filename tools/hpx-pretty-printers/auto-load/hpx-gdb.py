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
import sys
import os
import gdb

try:
    c_script = os.path.realpath(__file__)
    c_dir = os.path.dirname(c_script)
    py_dir = os.path.abspath(c_dir + '/../python')

    sys.path.append(py_dir)
except NameError:
    sys.path.append(os.getcwd() + '/../python')

try:
    from hpx_printers import register_hpx_printers
except ImportError:
    print('Unable to import the printers module. Add the printers directory to sys.path (python sys.path.append(PATH_TO_PRINTERS_DIRECTORY))')

register_hpx_printers(gdb.current_objfile())

