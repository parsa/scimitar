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

class FuturePrinter(object):
    def __init__(self, expr, val, tmpl):
        self.val = val
        self.expr = expr
        self.tmpl = tmpl
        self.px = val['shared_state_']['px']
        self.state_ = val['shared_state_']['px']['state_']
        self.storage_ = val['shared_state_']['px']['storage_']

    def display_hint(self):
        return self.expr

    def to_string(self):
        txt = 'px: %s, state: %s' % (gdb.parse_and_eval('%s' % self.px), self.state_,)
        return "(%s) {{ %s }}" % (self.expr, txt,)

    def children(self):
        result = []
        if self.tmpl == 'void':
            if bool(gdb.parse_and_eval('%d == 5' % (self.state_,))):
                result.extend([
                    ('value', '%s' % gdb.parse_and_eval('*((boost::exception_ptr*)(%s))' % (self.storage_.address,))),
                ])
        else:
            if bool(gdb.parse_and_eval('%d == 3' % (self.state_,))):
                value_t = gdb.lookup_type(self.tmpl)
                result.extend([
                    ('value', '%s' % gdb.parse_and_eval('*((%s *)%s)' % (value_t.tag, self.storage_.address,))),
                ])
            elif bool(gdb.parse_and_eval('%d == 5' % (self.state_,))):
                result.extend([
                    ('value', '%s' % gdb.parse_and_eval('*((boost::exception_ptr*)(%s))' % (self.storage_.address,))),
                ])
            else:
                result.extend([
                    ('value', 'N/A'),
                ])
        return result
printer_dict['hpx::lcos::(shared_)?future<(?P<tmpl>.*)>'] = FuturePrinter

