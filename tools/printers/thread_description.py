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

printer_dict = {}

class ThreadDescriptionPrinter(object):
    def __init__(self, expr, val):
        self.val = val
        self.expr = expr

    def display_hint(self):
        return self.expr

    def to_string(self):
        txt = ''
        if bool(gdb.parse_and_eval('type_ == 0')):
            txt = '[desc] {%s}' % gdb.parse_and_eval('data_.desc_')
        elif bool(gdb.parse_and_eval('type_ == 1')):
            txt = '[addr] {%s}' % gdb.parse_and_eval('(void*)data_.addr_')
                
        return "(%s) {{ %s }} %#02x" % (self.expr, txt, self.val.address)
printer_dict['hpx::util::thread_description'] = ThreadDescriptionPrinter

