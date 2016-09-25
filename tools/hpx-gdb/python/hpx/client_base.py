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
    def __init__(self, val):
        self.val = val
        self.shared_state_ = self.val['shared_state_']
        self.px = self.shared_state_['px']

        self.cond_1 = False
        self.cond_2 = False
        self.cond_3 = False
        if bool(gdb.parse_and_eval('%s != 0' % self.px)):
            self.cond_1 = True
            self.state_ = self.px['state_']

            if bool(gdb.parse_and_eval('%s == 3' % (self.state_,))):
                self.cond_2 = True
                self.buf = self.px['storage_']['data_']['buf']
            elif bool(gdb.parse_and_eval('%d == 5' % self.state_)):
                self.cond_3 = True
                self.buf = self.px['storage_']['data_']['buf']

    def to_string(self):
        txt = ''
        if self.cond_1:
            txt = str(self.state_)
        else:
            txt = 'empty'
                
        return "client_base: {{ %s }}" % (
            txt,
        )

    def children(self):
        result = [] 
        if self.cond_1:
            if self.cond_2:
                result.extend([
                    ('value', str(gdb.parse_and_eval('*((hpx::naming::id_type*)(%s))' % (self.buf,))),),
                ])
            elif self.cond_3:
                result.extend([
                    ('exception', str(gdb.parse_and_eval('*((boost::exception_ptr*)(%s))' % (self.buf,))),),
                ])
            result.extend([
                ('count', str(gdb.parse_and_eval(str(self.px['count_']))),),
            ])
                
        return result
printer_dict['hpx::components::client_base<(.+)>'] = ClientBasePrinter

