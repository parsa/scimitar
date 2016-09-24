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

class BacktracePrinter(object):
    def __init__(self, expr, val):
        self.val = val
        self.expr = expr

    def display_hint(self):
        return self.expr

    def to_string(self):
        txt = "{{ size=%s }}" % (
            gdb.parse_and_eval('%s' % (self.val['frames_']['_Mysize'],)),
        )
        return "(%s) {{ %s }}" % (self.expr, txt,)

    def children(self):
        result = [
            ('stacktrace', '%s,[%s]%s' % (
                gdb.parse_and_eval('%s' % (self.val['frames_']['_Myfirst'],)),
                gdb.parse_and_eval('%s' % (self.val['frames_']['_Mysize'],)),
                gdb.parse_and_eval('%s' % (self.val['stackTrace'],)))
            ),
        ]
                
        return result
printer_dict['hpx::util::backtrace'] = BacktracePrinter

