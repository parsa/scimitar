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

_eval_ = gdb.parse_and_eval

__printers__ = {}


class CombinedTaggedStatePrinter(object):

    def __init__(self, val):
        self.val = val
        # Values
        self.state_ = self.val['state_']
        self.state = _eval_(
            '(hpx::threads::thread_state_enum)((%s >> 56) & 0xff)' %
            self.state_
        )
        self.state_ex = _eval_(
            '(hpx::threads::thread_state_ex_enum)((%s >> 48) & 0xff)' %
            self.state_
        )
        self.tag = _eval_('%s & 0xffffffffffff' % self.state_)

    def to_string(self):
        txt = 'state=%s, state_ex=%s, tag=%s' % (
            self.state,
            self.state_ex,
            self.tag,
        )
        return "combined_tagged_state: {{ %s }}" % (txt, )

    def children(self):
        return [('state', str(self.state)),
                ('state_ex', str(self.state_ex)),
                ('tag', str(self.tag)), ]


__printers__['hpx::threads::detail::combined_tagged_state<'
             'enum hpx::threads::thread_state_enum, '
             'enum hpx::threads::thread_state_ex_enum '
             '>'] = CombinedTaggedStatePrinter


class AtomicCombinedTaggedStatePrinter(object):

    def __init__(self, val):
        self.val = val
        # Values
        self.m_storage = self.val['m_storage']
        self.state = _eval_(
            '(hpx::threads::thread_state_enum)((%s >> 56) & 0xff)' %
            self.m_storage
        )
        self.state_ex = _eval_(
            '(hpx::threads::thread_state_ex_enum)((%s >> 48) & 0xff)' %
            self.m_storage
        )
        self.tag = _eval_('%s & 0xffffffffffff' % self.m_storage)

    def to_string(self):
        txt = 'state=%s, state_ex=%s, tag=%s' % (
            self.state,
            self.state_ex,
            self.tag,
        )
        return  \
            "atomic<combined_tagged_state>: {{ %s }} %#02x" \
            % (txt, self.val.address)

    def children(self):
        return [('state', str(self.state)),
                ('state_ex', str(self.state_ex)),
                ('tag', str(self.tag)), ]


__printers__['boost::atomics::atomic<'
             'hpx::threads::detail::combined_tagged_state<'
             'enum hpx::threads::thread_state_enum, '
             'enum hpx::threads::thread_state_ex_enum'
             '>'
             '>'] = AtomicCombinedTaggedStatePrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
