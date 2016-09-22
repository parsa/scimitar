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
import sys, os

try:
    this_script = os.path.realpath(__file__)
    this_dir = os.path.dirname(this_script)

    sys.path.append(this_dir)
except NameError:
    sys.path.append(os.getcwd())

try:
    import printers
except ImportError:
    print('Unable to import the printers module. Add the printers directory to sys.path (python sys.path.append(PATH_TO_PRINTERS_DIRECTORY))')

