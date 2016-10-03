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


class HPXThread():

    class Context(object):

        def __init__(self):
            self._registers = {
                'pc': None,
                'r15': None,
                'r14': None,
                'r13': None,
                'r12': None,
                'rdx': None,
                'rax': None,
                'rbx': None,
                'rbp': None,
                'sp': None,
            }

            for reg in self._registers.iterkeys():
                self._registers[reg] = gdb.parse_and_eval('$' + reg)

        def __getattr__(self, name):
            if name == '_registers':
                return super(Context, self).__getattr__(name)
            return self._registers[name]

        def __setattr__(self, name, value):
            if name == '_registers':
                super(Context, self).__setattr__(name, value)
            elif self._registers.has_key(name):
                self._registers[name] = value
            else:
                raise Exception

        def __getitem__(self, key):
            return self._registers[key]

        def __setitem__(self, key, value):
            self._registers[key] = value

        def switch(self):
            prev_ctx = HPXThread.Context()

            for rk, rv in self._registers.iteritems():
                gdb.execute(
                    "set $%s = 0x%x" % (rk, int("%d" % rv) & (2 ** 64 - 1))
                )

            return prev_ctx

    def __init__(self, thread_data_base):
        self.base_type = gdb.lookup_type("hpx::threads::thread_data_base")
        if thread_data_base.type != self.base_type.pointer():
            if thread_data_base.type == self.base_type:
                thread_data_base = thread_data_base.address()
            else:
                thread_data_base = thread_data_base.reinterpret_cast(
                    self.base_type.pointer()
                )

        self.thread_data = thread_data_base.cast(
            thread_data_base.dynamic_type
        ).dereference()

        context_impl = self.thread_data['coroutine_']['m_pimpl']['px']
        self.stack_end = context_impl['m_stack'] + context_impl['m_stack_size']
        self.stack_start = context_impl['m_stack']
        self.m_sp = context_impl['m_sp']

        assert thread_data_base == context_impl['m_thread_id']
        self.id = thread_data_base #context_impl['m_thread_id']
        self.parent_id = self.thread_data['parent_thread_id_']
        self.description = self.thread_data['description_']
        self.lco_description = self.thread_data['lco_description_']

        current_state = self.thread_data['current_state_']

        tagged_state_type = current_state.type.template_argument(0)
        state_enum_type = tagged_state_type.template_argument(0)
        self.state = current_state['m_storage'] >> 24
        self.state = self.state.cast(state_enum_type)

        current_state_ex = self.thread_data['current_state_ex_']
        tagged_state_ex_type = current_state_ex.type.template_argument(0)
        state_ex_enum_type = tagged_state_ex_type.template_argument(0)
        self.state_ex = current_state_ex['m_storage'] >> 24
        self.state_ex = self.state_ex.cast(state_ex_enum_type)

        self.size_t = gdb.lookup_type("std::size_t")
        stack = self.m_sp.reinterpret_cast(self.size_t)

        self.context = self.Context()
        self.context.pc = self.deref_stack(stack + (8 * 8))
        self.context.r15 = self.deref_stack(stack + (8 * 0))
        self.context.r14 = self.deref_stack(stack + (8 * 1))
        self.context.r13 = self.deref_stack(stack + (8 * 2))
        self.context.r12 = self.deref_stack(stack + (8 * 3))
        self.context.rdx = self.deref_stack(stack + (8 * 4))
        self.context.rax = self.deref_stack(stack + (8 * 5))
        self.context.rbx = self.deref_stack(stack + (8 * 6))
        self.context.rbp = self.deref_stack(stack + (8 * 7))
        self.context.sp = stack + (8 * 8)

        prev_context = self.context.switch()
        frame = gdb.newest_frame()
        function_name = frame.name()
        p = re.compile("^hpx::util::coroutines.*$")

        try:
            while p.match(function_name):
                if frame.older() is None:
                    break
                frame = frame.older()
                function_name = frame.name()

            if not frame.older() is None:
                frame = frame.older()
                function_name = frame.name()

            line = frame.function().line
            filename = frame.find_sal().symtab.filename

            self.pc_string = "0x%x in " % frame.pc(
            ) + "%s at " % function_name + "%s:" % filename + "%d" % line
        except:
            self.pc_string = "0x%x in " % frame.pc() + "<unkown>"

        self.frame = frame

        prev_context.switch()

    def deref_stack(self, addr):
        return addr.reinterpret_cast(self.size_t.pointer()).dereference()

    def info(self):
        print(" Thread 0x%x" % self.id)
        if self.m_sp.reinterpret_cast(self.m_sp.dereference().type
                                      ) > self.stack_end:
            print(" This thread has a stack overflow")
        print("  parent thread = %s" % self.parent_id)
        print("  description = " + self.description.string())
        print("  lco_description = " + self.lco_description.string())
        print("  state = %s" % self.state)
        print("  state_ex = %s" % self.state_ex)
        print("  pc = %s" % self.pc_string)

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
