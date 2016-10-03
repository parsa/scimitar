# -*- coding: utf-8 -*-
'''
    Scimitar: Ye Distributed Debugger
    ~~~~~~~~
    :copyright:
    Copyright (c) 2014 Thomas Heller
    Copyright (c) 2016 Parsa Amini
    Copyright (c) 2016 Hartmut Kaiser
    :license:
    Distributed under the Boost Software License, Version 1.0. (See accompanying
    file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

hpx.py - A set of functions to help debug a HPX binary inside of GDB
'''

import gdb
import re
import threading
from hpx import gdb_cmd_type
from hpx.printers.boost import Set

class HPX(gdb.Command):
  "Commands to introspect the state of a HPX program."
  def __init__(self):
    gdb.Command.__init__(self, "hpx", gdb_cmd_type, gdb.COMPLETE_NONE, True)

#  def invoke(self, arg, from_tty):
#    print("Hello World")

class HPXList(gdb.Command):
  "List various HPX states"
  def __init__(self):
    super(HPXList, self).__init__("hpx list", gdb_cmd_type, gdb.COMPLETE_NONE, True)

  def invoke(self, arg, from_tty):
    print("Hello World")


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
        if self.m_sp.reinterpret_cast(self.m_sp.dereference().type) > self.stack_end:
            print(" This thread has a stack overflow")
        print("  parent thread = %s" % self.parent_id)
        print("  description = " + self.description.string())
        print("  lco_description = " + self.lco_description.string())
        print("  state = %s" % self.state)
        print("  state_ex = %s" % self.state_ex)
        print("  pc = %s" % self.pc_string)


class HPXListThreads(gdb.Command):
    '''
    Get the list of all HPX threads on this locality
    '''

    def __init__(self):
        super(HPXListThreads, self).__init__(
            "hpx list threads", gdb_cmd_type, gdb.COMPLETE_NONE, False
        )

    def deref_stack(self, addr):
        return addr.reinterpret_cast(gdb.lookup_type("std::size_t").pointer()
                                     ).dereference()

    def invoke(self, arg, from_tty):
        #gdb.selected_frame().read_var("hpx::runtime::runtime_")
        runtime = gdb.lookup_global_symbol("hpx::runtime::runtime_").value(
        )["ptr_"].dereference()
        #gdb.selected_frame().read_var("hpx::runtime::runtime_.ptr_").dereference()#["ptr_"]
        thread_manager_ptr = runtime.cast(runtime.dynamic_type)["thread_manager_"]['px']
        thread_manager = thread_manager_ptr.cast(
            thread_manager_ptr.dynamic_type
        ).dereference()

        scheduler = thread_manager['pool_']['sched_']
        scheduler_type = scheduler.type.target() #.target()

        queues = {}
        for f in scheduler_type.fields():
            if f.name == "high_priority_queues_":
                queues[f.name] = scheduler[f.name]
            if f.name == "low_priority_queue_":
                queues[f.name] = scheduler[f.name]
            if f.name == "queues_":
                queues[f.name] = scheduler[f.name]

        for name in queues:
            if name == "queues_":
                item = queues[name]['_M_impl']['_M_start']
                end = queues[name]['_M_impl']['_M_finish']

                count = 0
                while not item == end:
                    print("Thread queue %d:" % count)
                    thread_map = Set(
                        item.dereference().dereference()['thread_map_']
                    )
                    for k, v in thread_map:
                        thread = HPXThread(v['px'])

                        thread.info()
                        print("")
                    item = item + 1
                    count = count + 1
            if name == "high_priority_queues_":
                item = queues[name]['_M_impl']['_M_start']
                end = queues[name]['_M_impl']['_M_finish']

                count = 0
                while not item == end:
                    print("High Priority Thread queue %d:" % count)
                    thread_map = Set(
                        item.dereference().dereference()['thread_map_']
                    )
                    for k, v in thread_map:
                        thread = HPXThread(v['px'])

                        thread.info()
                        print("")
                    item = item + 1
                    count = count + 1

        print("Low priority queue:")
        thread_map = Set(queues["low_priority_queue_"]['thread_map_'])
        for k, v in thread_map:
            thread = HPXThread(v['px'])

            thread.info()
            print("")


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
            if not self.context is None:
                for os_thread in self.context:
                    ctx = self.context[os_thread]
                    gdb.execute("thread %d" % os_thread, False, True)
                    ctx.switch()
                self.context = None
        finally:
            gdb.execute("thread %d" % cur_os_thread, False, True)
            self.lock.release()


state = HPXGdbState()


class HPXSelectThread(gdb.Command):
    '''
    This command let's you overwrite the current frame with a suspended HPX thread.
    To get a list of currently running hpx threads see 'hpx list threads'.

    Arguments:
       <thread-id>: A thread id to switch to
       restore: Restores the state of the overwritten threads
    '''

    def __init__(self):
        super(HPXSelectThread, self).__init__(
            "hpx thread", gdb_cmd_type, gdb.COMPLETE_NONE, False
        )

    def deref_stack(self, addr):
        return addr.reinterpret_cast(gdb.lookup_type("std::size_t").pointer()
                                     ).dereference()

    def invoke(self, arg, from_tty):
        argv = gdb.string_to_argv(arg)
        if len(argv) != 1:
            print(
                "Error: You need to supply at least one argument. See help hpx thread"
            )
            return

        if argv[0] == "restore":
            state.restore()
            return

        if argv[0][0] == '0' and argv[0][1] == 'x':
            thread_id = gdb.Value(int(argv[0], 16))
        else:
            thread_id = gdb.Value(int(argv[0]))

        thread = HPXThread(thread_id)

        print("Switched to HPX Thread 0x%x" % thread_id)
        print(thread.pc_string)

        state.save_context(thread.context.switch())


def restore_context(event):
    state.restore()


class HPXContinue(gdb.Command):
    '''
    Similiar to 'continue' but restores any selected HPX threads before continuing.
    '''

    def __init__(self):
        super(HPXContinue, self).__init__(
            "hpx continue", gdb_cmd_type, gdb.COMPLETE_NONE, False
        )

    def invoke(self, arg, from_tty):
        argv = gdb.string_to_argv(arg)
        state.restore()

        #gdb.execute("thread 15", False, True)
        #cur_os_thread = gdb.selected_thread().num

        frame = gdb.newest_frame()

        handle_attach = False
        count = 0
        while True:
            function = frame.function()
            if function and function.name == "hpx::util::command_line_handling::handle_attach_debugger()":
                handle_attach = True
                break
            frame = frame.older()
            if not frame or count > 5:
                break
            count = count + 1

        if handle_attach:
            frame.select()
            gdb.execute("set var i = 1", True)

        #gdb.execute("thread %d" % cur_os_thread, False, True)

        if len(argv) == 0:
            print("Continuing...")
            gdb.execute("continue")
        else:
            if argv[0] != "hook":
                print("wrong argument ...")


HPX()
HPXList()
HPXListThreads()
HPXSelectThread()
HPXContinue()

#gdb.events.cont.connect(restore_context)
