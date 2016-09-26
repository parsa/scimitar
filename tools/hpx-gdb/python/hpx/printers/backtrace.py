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
        self._Myfirst = self.frames_['_Myfirst']
        self._Mysize = self.frames_['_Mysize']
        self.stackTrace = self.val['stackTrace']

    def to_string(self):
        txt = "{{ size=%s }}" % (
            self.frames_['_Mysize'],
        )
        return "backtrace: {{ %s }}" % (txt,)

    def children(self):
        result = [
            ('stacktrace',
                '%s,[%s]%s' % (
                    self._Myfirst,
                    self._Mysize,
                    self.stackTrace,
                ),
            ),
        ]
                
        return result
printer_dict['hpx::util::backtrace'] = BacktracePrinter

