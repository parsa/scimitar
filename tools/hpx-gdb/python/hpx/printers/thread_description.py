# coding: utf-8
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

_eval_ = gdb.parse_and_eval

printer_dict = {}


class ThreadDescriptionPrinter(object):

    def __init__(self, val):
        self.val = val
        # Values
        self.type_ = self.val['type_']
        self.data_ = self.val['data_']
        self.desc_ = self.data_['desc_']
        self.addr_ = self.data_['addr_']
        # Conditions
        self.is_type_0 = bool(_eval_('%s == 0' % self.type_))
        self.is_type_1 = bool(_eval_('%s == 1' % self.type_))

    def to_string(self):
        txt = ''
        if self.is_type_0:
            txt = '[desc] {%s}' % self.desc_
        elif self.is_type_1:
            txt = '[addr] {%s}' % _eval_('(void*)%s' % self.addr_)

        return "thread_description {{ %s }}" % (txt, )


printer_dict['hpx::util::thread_description'] = ThreadDescriptionPrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
