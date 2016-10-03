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


class GidTypePrinter(object):

    def __init__(self, val):
        self.val = val
        # Values
        self.id_msb_ = self.val['id_msb_']
        self.id_lsb_ = self.val['id_lsb_']
        # Conditions
        self.cond_1 = bool(
            _eval_('(%d & 0x40000000ull) != 0' % (self.id_msb_, ))
        )
        self.cond_2 = bool(
            _eval_('((%s >> 32) & 0xffffffffull) != 0' % self.id_msb_)
        )
        if self.cond_1:
            self.log2credits = _eval_(
                '(%d >> 24) & 0x1full' % (self.id_msb_, )
            )
            self.credits = _eval_(
                '1ull << ((%d >> 24) & 0x1full)' % (self.id_msb_, )
            )
            self.was_split = _eval_(
                '(%d & 0x80000000ull) ? true : false' % (self.id_msb_, )
            )
        if self.cond_2:
            self.locality_id = _eval_(
                '((%s >> 32) & 0xffffffffull) - 1' % (self.id_msb_, )
            )
        self.msb = _eval_('%s & 0x7fffffull' % (self.id_msb_, ))
        self.lsb = _eval_('%s' % (self.id_lsb_), )
        self.has_credit = _eval_(
            '(%s & 0x40000000ull) ? true : false' % (self.id_msb_, )
        )
        self.is_locked = _eval_(
            '(%s & 0x20000000ull) ? true : false' % (self.id_msb_, )
        )
        self.dont_cache = _eval_(
            '(%s & 0x00800000ull) ? true : false' % (self.id_msb_, )
        )

    def to_string(self):
        return "gid_type: {{ msb=%#02x lsb=%#02x }}" % (
            self.id_msb_,
            self.id_lsb_,
        )

    def children(self):
        result = []
        if self.cond_1:
            result.extend([('log2credits', str(self.log2credits)),
                           ('credits', '%#02x' % self.credits),
                           ('was_split', str(self.was_split)), ])
        if self.cond_2:
            result.extend([('locality_id', str(self.locality_id)), ])
        result.extend([('msb', '%#02x' % self.msb),
                       ('lsb', '%#02x' % self.lsb),
                       ('has_credit', str(self.has_credit)),
                       ('is_locked', str(self.is_locked)),
                       ('dont_cache', str(self.dont_cache)), ])
        return result


__printers__['hpx::naming::gid_type'] = GidTypePrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
