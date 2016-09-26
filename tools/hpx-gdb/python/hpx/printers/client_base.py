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

_eval_ = gdb.parse_and_eval

printer_dict = {}

class ClientBasePrinter(object):
    def __init__(self, val):
        self.val = val
        # Values
        self.shared_state_ = self.val['shared_state_']
        self.px = self.shared_state_['px']
        self.state_ = self.px['state_']
        # Conditions
        self.cond_1 = bool(_eval_('%s != 0' % self.px))
        self.cond_2 = bool(_eval_('%s == 3' % self.state_))
        self.cond_3 = bool(_eval_('%d == 5' % self.state_))
        if self.cond_1:
            self.count_ = self.px['count_']

            if self.cond_2:
                self.buf = self.px['storage_']['data_']['buf']
                self.value = _eval_(
                    '*((hpx::naming::id_type*)(%s))' % (self.buf,)
                )
            if self.cond_3:
                self.buf = self.px['storage_']['data_']['buf']
                self.exception = _eval_(
                    '*((boost::exception_ptr*)(%s))' % (self.buf,)
                )

    def to_string(self):
        txt = ''
        if self.cond_1:
            txt = str(self.state_)
        else:
            txt = 'empty'
                
        return "client_base: {{ %s }}" % ( txt, )

    def children(self):
        result = [] 
        if self.cond_1:
            if self.cond_2:
                result.extend([
                    ( 'value', str(self.value) ),
                ])
            elif self.cond_3:
                result.extend([
                    ( 'exception', str(self.exception) ),
                ])
            result.extend([
                ( 'count', str(self.count_) ),
            ])
                
        return result
printer_dict['hpx::components::client_base<(.+)>'] = ClientBasePrinter

