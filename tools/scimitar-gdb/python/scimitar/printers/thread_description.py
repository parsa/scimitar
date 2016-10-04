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

_eval_ = gdb.parse_and_eval


class ThreadDescriptionPrinter(object):

    def __init__(self, val, type_):
        self.val = val
        self.type_ = type_
        # Values
        self.type_ = self.val['type_']
        self.data_ = self.val['data_']
        self.desc_ = self.data_['desc_']
        self.addr_ = self.data_['addr_']

        # Conditions
        # enum hpx::util::thread_description::data_type
        #   data_type_description = 0
        #   data_type_address = 1
        self.is_description = bool(self.type_ == 0)
        self.is_address = bool(self.type_ == 1)

    def to_string(self):
        txt = ''
        if self.is_description:
            txt = '[desc] {%s}' % self.desc_
        else:
            txt_t = gdb.lookup_type('void').pointer()
            txt = '[addr] {%s}' % self.addr_.cast(txt_t)

        return "%s {{ %s }}" % (self.type_, txt, )


scimitar.pretty_printers['hpx::util::thread_description'] = ThreadDescriptionPrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
