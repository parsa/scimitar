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

class TupleMemberPrinter(object):
    def __init__(self, val):
        self.val = val
        # Get the template types
        self.tmpl = []
        for i in range(10):
            try:
                self.tmpl.append(str(self.val.type.template_argument(i)))
            except RuntimeError:
                break

    def to_string(self):
        txt = ''
        try:
            txt = str(self.val['_value'])
        except gdb.error:
            try:
                txt = '%s' % _eval_('*(%s *)%s' % (self.tmpl[1], self.val))
            except gdb.error:
                pass
                
        return "tuple_member: {{ %s }}" % (self.txt,)
printer_dict['hpx::util::detail::tuple_member<.+>'] = TupleMemberPrinter

class TuplePrinter(object):
    def __init__(self, val):
        self.val = val
        # Values
        self._imp = self.val['_impl']
        # Get the template types
        self.tmpl = []
        for i in range(10):
            try:
                self.tmpl.append(str(self.val.type.template_argument(i)))
            except RuntimeError:
                break

    def to_string(self):
        parts = [
            '%s'
            % _eval_(
                '(hpx::util::detail::tuple_member<%d,%s,void>&)%s'
                % (i, t, self._impl)
            ) for i, t in enumerate(self.tmpl)
        ]
        txt = ', '.join(parts)
                
        return "tuple {{ %s }}" % (txt,)

    def children(self):
        result = [] 
        for i, t in enumerate(self.tmpl):
            result.extend([
                (
                    '%d' % i,
                    str(_eval_(
                        '(hpx::util::detail::tuple_member<%d,%s,void>&)%s'
                        % (i, t, self._impl)
                    ))),
            ])
                
        return result
printer_dict['hpx::util::tuple<.+>'] = TuplePrinter

