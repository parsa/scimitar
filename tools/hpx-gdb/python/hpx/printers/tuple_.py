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
import hpx

_eval_ = gdb.parse_and_eval


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

        return "tuple_member: {{ %s }}" % (txt, )


hpx.pretty_printers['hpx::util::detail::tuple_member<.+>'] = TupleMemberPrinter


class TuplePrinter(object):

    def __init__(self, val):
        self.val = val
        # Values
        self._impl = self.val['_impl']
        # Get the template types
        self.tmpl = []
        for i in range(10):
            try:
                self.tmpl.append(str(self.val.type.template_argument(i)))
            except RuntimeError:
                break

        self.items = []
        for i, t in enumerate(self.tmpl):
            #Tp = gdb.lookup_type(
            #    '(hpx::util::detail::tuple_member<%s,%s,void>&)' % (i, t)
            #)
            #self.items.append(str(t.cast(Tp)))
            self.items.append(str(t))

    def to_string(self):
        txt = ', '.join(self.items)

        return "tuple {{ %s }}" % (txt, )

    def display_hint(self):
        return 'map'

    def children(self):
        result = []
        for i, j in enumerate(self.items):
            result += [(str(i),
                        j, )]

        return result


__printers__['hpx::util::tuple<.+>'] = TuplePrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
