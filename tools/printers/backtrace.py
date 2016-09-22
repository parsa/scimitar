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
import re
import sys
import datetime
import ctypes

class BacktracePrinter(object):
    def __init__(self, expr, val):
        self.val = val
        self.expr = expr
        self.frames_ = val['frames_']
        self.stackTrace = val['stackTrace']

    def display_hint(self):
        return self.expr

    def to_string(self):
        mysize = self.frames_['_Mysize']
        return "(%s) {{ %s }} %#02x" % (self.expr, str(mysize), self.val.address)

    def children(self):
        result = [
            ('stacktrace', '%s,[%s]%s' % (self.frames_['_Myfirst'], self.frames_['_Mysize'], self.stackTrace)),
        ]
                
        return result

def lookup_type(val):
    type_ = val.type

    if type_.code == gdb.TYPE_CODE_PTR:
        type_ = type.dereference()

    type_ = type_.unqualified().strip_typedefs()

    expr = str(type_)
    m = re.match('^(const )?hpx::util::backtrace( \*)?( const)?$', expr)
    if m:
        return BacktracePrinter(expr, val)
    return None

gdb.pretty_printers.append(lookup_type)

