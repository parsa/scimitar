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

class ThreadDescriptionPrinter(object):
    def __init__(self, expr, val):
        self.val = val
        self.expr = expr
        self.type_ = val['type_']

    def display_hint(self):
        return self.expr

    def to_string(self):
        state_ = None
        o = ''
        if int(self.type_) == 0:
            o = '[desc] {%s}' % self.val['data_']['desc_']
        elif int(self.type_) == 1:
            t = gdb.lookup_type('void').pointer()
            o = '[addr] {%s}' % self.val['data_']['addr_'].cast(t)
                
        return "(%s) {{ %s }} %#02x" % (self.expr, o, self.val.address)

def lookup_type(val):
    type_ = val.type

    if type_.code == gdb.TYPE_CODE_PTR:
        type_ = type.dereference()

    type_ = type_.unqualified().strip_typedefs()

    expr = str(type_)
    m = re.match('^(const )?hpx::util::thread_description( \*)?( const)?$', expr)
    if m:
        return ThreadDescriptionPrinter(expr, val)
    return None

gdb.pretty_printers.append(lookup_type)

