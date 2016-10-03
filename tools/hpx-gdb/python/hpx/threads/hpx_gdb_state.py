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
import threading


class HPXGdbState():

    def __init__(self):
        self.context = None
        self.lock = threading.Lock()

    def save_context(self, ctx):
        if self.context is None:
            self.context = {}

        os_thread = gdb.selected_thread().num
        if os_thread in self.context:
            return

        self.context[os_thread] = ctx

    def restore(self):
        self.lock.acquire()
        cur_os_thread = gdb.selected_thread().num
        try:
            if self.context is not None:
                for os_thread in self.context:
                    ctx = self.context[os_thread]
                    gdb.execute("thread %d" % os_thread, False, True)
                    ctx.switch()
                self.context = None
        finally:
            gdb.execute("thread %d" % cur_os_thread, False, True)
            self.lock.release()

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
