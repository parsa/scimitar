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


class FuturePrinter(object):

    def __init__(self, val):
        self.val = val
        # Values
        self.px = self.val['shared_state_']['px']
        self.state_ = self.px['state_']
        self.storage_ = self.px['storage_']
        # Template type
        self.tmpl = str(self.val.type.template_argument(0))
        # Conditions
        self.is_void = self.tmpl == 'void'
        self.is_state_5 = bool(_eval_('%d == 5' % (self.state_, )))
        self.is_state_3 = bool(_eval_('%d == 3' % (self.state_, )))

        if self.is_void:
            if self.is_state_5:
                self.value = _eval_(
                    '*((boost::exception_ptr*)(%s))' %
                    (self.storage_.address, )
                )
        else:
            if self.is_state_3:
                self.value = _eval_(
                    '*((%s *)%s)' % (value_t.tag,
                                     self.storage_.address, )
                )
            if self.is_state_5:
                self.value = _eval_(
                    '*((boost::exception_ptr*)(%s))' %
                    (self.storage_.address, )
                )

    def to_string(self):
        txt = 'px: %s, state: %s' % (self.px,
                                     self.state_, )
        return "future: {{ %s }}" % (txt, )

    def children(self):
        result = []
        if self.is_void:
            if self.is_state_5:
                result.extend([('value', str(self.value)), ])
        else:
            if self.is_state_3:
                value_t = gdb.lookup_type(self.tmpl)
                result.extend([('value', str(self.value)), ])
            elif self.is_state_5:
                result.extend([('value', self.value), ])
            else:
                result.extend([('value', 'N/A'), ])
        return result


printer_dict['hpx::lcos::(shared_)?future<.+>'] = FuturePrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
