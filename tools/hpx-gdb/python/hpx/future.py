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
    def __init__(self, val):
        self.val = val
        self.tmpl = str(self.val.type.template_argument(0))
        self.px = self.val['shared_state_']['px']
        self.state_ = self.px['state_']
        self.storage_ = self.px['storage_']

        self.cond_1 = False
        self.cond_2 = False
        self.cond_3 = False
        if self.tmpl == 'void':
            self.cond_1 = True
        if bool(gdb.parse_and_eval('%d == 5' % (self.state_,))):
            self.cond_2 = True
        if bool(gdb.parse_and_eval('%d == 3' % (self.state_,))):
            self.cond_3 = True

    def to_string(self):
        txt = 'px: %s, state: %s' % (self.px, self.state_,)
        return "future: {{ %s }}" % (txt,)

    def children(self):
        result = []
        if self.cond_1:
            if self.cond_2:
                result.extend([
                    ('value', '%s' % gdb.parse_and_eval('*((boost::exception_ptr*)(%s))' % (self.storage_.address,))),
                ])
        else:
            if self.cond_3:
                value_t = gdb.lookup_type(self.tmpl)
                result.extend([
                    ('value', '%s' % gdb.parse_and_eval('*((%s *)%s)' % (value_t.tag, self.storage_.address,))),
                ])
            elif self.cond_2:
                result.extend([
                    ('value', '%s' % gdb.parse_and_eval('*((boost::exception_ptr*)(%s))' % (self.storage_.address,))),
                ])
            else:
                result.extend([
                    ('value', 'N/A'),
                ])
        return result
printer_dict['hpx::lcos::(shared_)?future<.*>'] = FuturePrinter

