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

class FuturePrinter(object):
    def __init__(self, expr, val, tmpltype):
        self.val = val
        self.expr = expr
        self.tmpltype = tmpltype
        self.px = val['shared_state_']['px']
        self.state = val['shared_state_']['px'].dereference()['state_']

    def display_hint(self):
        return self.expr

    def to_string(self):
        return "(%s) {{ %s }} %#02x" % (self.expr, str(self.state), self.val.address)

    def children(self):
        state = int(self.state)
        result = []
        if self.tmpltype == 'void':
            # FIXME: Something's not right here
            if state == 5:
                result.extend([
                    ('value', self.px.dereference()['storage_']),
                ])
        else:
            if state == 3:
                result.extend([
                    ('value', self.px.dereference()['storage_']),
                ])
            elif state == 5:
                result.extend([
                    ('value', self.px.dereference()['storage_']),
                ])
                
        return result

def lookup_type(val):
    type_ = val.type

    if type_.code == gdb.TYPE_CODE_PTR:
        type_ = type.dereference()

    type_ = type_.unqualified().strip_typedefs()

    expr = str(type_)
    m = re.match('^(const )?hpx::lcos::(shared_)?future<(?P<type>\w*)>( \*)?( const)?$', expr)
    if m:
        return FuturePrinter(expr, val, m.group('type'))
    return None

gdb.pretty_printers.append(lookup_type)

