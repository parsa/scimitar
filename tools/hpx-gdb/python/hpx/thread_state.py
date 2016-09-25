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

class CombinedTaggedStatePrinter(object):
    def __init__(self, val):
        self.val = val
        self.state_ = self.val['state_']

    def to_string(self):
        txt = 'state=%s, stateex=%s, tag=%s' % (
            gdb.parse_and_eval('(hpx::threads::thread_state_enum)((%s >> 56) & 0xff)' % self.state_),
            gdb.parse_and_eval('(hpx::threads::thread_state_ex_enum)((%s >> 48) & 0xff)' % self.state_),
            gdb.parse_and_eval('%s & 0xffffffffffff' % self.state_),
        )
        return "combined_tagged_state: {{ %s }}" % (txt,)

    def children(self):
        return [
            ('state', str(gdb.parse_and_eval('(hpx::threads::thread_state_enum)((%s >> 56) & 0xff)' % self.state_)),),
            ('stateex', str(gdb.parse_and_eval('(hpx::threads::thread_state_ex_enum)((%s >> 48) & 0xff)' % self.state_)),),
            ('tag', str(gdb.parse_and_eval('%s & 0xffffffffffff' % self.state_)),),
        ]
printer_dict['hpx::threads::detail::combined_tagged_state<enum hpx::threads::thread_state_enum, enum hpx::threads::thread_state_ex_enum>'] = CombinedTaggedStatePrinter

class AtomicCombinedTaggedStatePrinter(object):
    def __init__(self, val):
        self.val = val
        self.m_storage = self.val['m_storage']

    def to_string(self):
        txt = 'state=%s, stateex=%s, tag=%s' % (
            gdb.parse_and_eval('(hpx::threads::thread_state_enum)((%s >> 56) & 0xff)' % self.m_storage),
            gdb.parse_and_eval('(hpx::threads::thread_state_ex_enum)((%s >> 48) & 0xff)' % self.m_storage),
            gdb.parse_and_eval('%s & 0xffffffffffff' % self.m_storage),
        )
        return "atomic<combined_tagged_state>: {{ %s }} %#02x" % (txt, self.val.address)

    def children(self):
        return [
            ('state', str(gdb.parse_and_eval('(hpx::threads::thread_state_enum)((%s >> 56) & 0xff)' % self.m_storage)),),
            ('stateex', str(gdb.parse_and_eval('(hpx::threads::thread_state_ex_enum)((%s >> 48) & 0xff)' % self.m_storage)),),
            ('tag', str(gdb.parse_and_eval('%s & 0xffffffffffff' % self.m_storage)),),
        ]
printer_dict['boost::atomics::atomic<hpx::threads::detail::combined_tagged_state<enum hpx::threads::thread_state_enum, enum hpx::threads::thread_state_ex_enum>>'] = AtomicCombinedTaggedStatePrinter

