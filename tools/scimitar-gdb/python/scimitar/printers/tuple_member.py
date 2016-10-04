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


class TupleMemberPrinter(object):

    def __init__(self, val, type_):
        self.val = val
        self.type_ = type_
        # Get the template types
        self.tmpl = []
        for i in range(10):
            try:
                self.tmpl.append(str(self.val.type.template_argument(i)))
            except RuntimeError:
                break

    def to_string(self):
        display_string = ''
        try:
            tmpl_t = gdb.lookup_type(self.tmpl[1]).pointer()
            display_string = str(self.val.cast(tmpl_t).dereference())
        except gdb.error:
            pass
        try:
            display_string = str(self.val['_value'])
        except gdb.error:
            pass

        return "%s: {{ %s }}" % (self.type_, display_string, )


scimitar.pretty_printers['hpx::util::detail::tuple_member<.+>'] = TupleMemberPrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
