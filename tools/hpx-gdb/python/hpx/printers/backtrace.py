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

printer_dict = {}

class BacktracePrinter(object):
    def __init__(self, val):
        self.val = val
        
        self.frames_ = self.val['frames_']

        self.frames_vis = gdb.default_visualizer(self.frames_)

    def to_string(self):
        return "hpx::util::backtrace wrapping: {{ %s }}" % (
            self.frames_vis.to_string(), 
        )

    def children (self):
        return self.frames_vis.children()

printer_dict['hpx::util::backtrace'] = BacktracePrinter

