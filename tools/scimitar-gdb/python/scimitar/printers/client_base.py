# -*- coding: utf-8 -*-
#
# Scimitar: Ye Distributed Debugger
# 
# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#
import gdb
import scimitar


class ClientBasePrinter(object):

    def __init__(self, val, type_):
        self.val = val
        self.type_ = type_
        # Values
        self.px = self.val['shared_state_']['px']
        self.state_ = self.px['state_']
        self.print_values = []
        # Conditions
        if bool(self.px == 0):
            self.display_string = '(empty)'
        else:
            self.display_string = self.state_
            if bool(self.state_ == 3):
                self.buf = self.px['storage_']['__data']
                T_id_type = gdb.lookup_type('hpx::naming::id_type').pointer()
                self.print_values.extend([('value', self.buf.cast(T_id_type).dereference()), ])
            elif bool(self.state_ == 5):
                self.buf = self.px['storage_']['__data']
                T_exception_ptr = gdb.lookup_type('boost::exception_ptr').pointer()
                self.print_value.extend( [(
                    'exception', self.buf.cast(T_exception_ptr).dereference()
                ), ])
            self.print_values.extend([('count', self.px['count_']), ])

    def to_string(self):
        display_string = ''
        return "%s: {{ %s }} %s" % (
            self.type_,
            self.display_string,
            self.val.address,
        )

    def children(self):
        return self.print_values


scimitar.pretty_printers['hpx::components::client_base<(.+)>'
                         ] = ClientBasePrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
