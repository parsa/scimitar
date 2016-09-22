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

class ClientBasePrinter(object):
    def __init__(self, expr, val):
        self.val = val
        self.expr = expr

    def display_hint(self):
        return self.expr

    def to_string(self):
        state_ = None
        txt = ''
        if bool(gdb.parse_and_eval('shared_state_.px != 0')):
            txt = '%s' % gdb.parse_and_eval('shared_state_.px->state_')
        else:
            txt = 'empty'
                
        return "(%s) {{ %s }} %#02x" % (self.expr, txt, self.val.address)

    def children(self):
        result = [] 
        if bool(gdb.parse_and_eval('shared_state_.px != 0')):
            state_ = int(self.px['state_'])
            if bool(gdb.parse_and_eval('shared_state_.px->state_ == 3')):
                result.extend([
                    ('value', '%s' % gdb.parse_and_eval('*((hpx::naming::id_type*)(shared_state_.px->storage_.data_.buf))')),
                ])
            elif bool(gdb.parse_and_eval('shared_state_.px->state_ == 5')):
                result.extend([
                    ('exception', '%s' % gdb.parse_and_eval('*((boost::exception_ptr*)(shared_state_.px->storage_.data_.buf))')),
                ])
            result.extend([
                ('count', '%s' % gdb.parse_and_eval('shared_state_.px->count_')),
            ])
                
        return result
printer_dict['hpx::components::client_base<(.*)>'] = ClientBasePrinter

