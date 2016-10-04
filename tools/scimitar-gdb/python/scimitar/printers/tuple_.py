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


class TuplePrinter(object):

    def __init__(self, val, type_):
        self.val = val
        self.type_ = type_
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
        display_string = ', '.join(self.items)

        return "%s {{ %s }} %s" % (self.type_, display_string, self.val.address)

    def display_hint(self):
        return 'map'

    def children(self):
        result = []
        for i, j in enumerate(self.items):
            result += [(str(i),
                        j, )]

        return result


scimitar.pretty_printers['hpx::util::tuple<.+>'] = TuplePrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
