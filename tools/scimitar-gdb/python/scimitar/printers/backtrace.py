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


class BacktracePrinter(object):

    def __init__(self, val, type_):
        self.val = val
        self.type_ = type_

        self.frames_ = self.val['frames_']
        self.frames_vis = gdb.default_visualizer(self.frames_)

    def to_string(self):
        return "%s wrapping: {{ %s }}  %s" % (
            self.type_,
            self.frames_vis.to_string(),
            self.val.address,
        )

    def children(self):
        return self.frames_vis.children()


scimitar.pretty_printers['hpx::util::backtrace'] = BacktracePrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
