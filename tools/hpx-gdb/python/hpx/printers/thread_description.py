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
    def __init__(self, val):
        self.val = val

        self.cond_1 = True
        self.cond_2 = True
        if bool(gdb.parse_and_eval('%s == 0' % self.val['type_'])):
            self.cond_1 = True
        elif bool(gdb.parse_and_eval('%s == 1' % self.val['type_'])):
            self.cond_2 = True

    def to_string(self):
        txt = ''
        if self.cond_1:
            txt = '[desc] {%s}' % gdb.parse_and_eval(
                '%s' % self.val['data_']['desc_']
            )
        elif self.cond_2:
            txt = '[addr] {%s}' % gdb.parse_and_eval(
                '(void*)%s' % self.val['data_']['addr_']
            )
                
        return "thread_description {{ %s }}" % (txt,)
printer_dict['hpx::util::thread_description'] = ThreadDescriptionPrinter

