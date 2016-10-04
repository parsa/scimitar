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


class GidTypePrinter(object):

    def __init__(self, val, type_):
        self.val = val
        self.type_ = type_
        # Values
        self.id_msb_ = self.val['id_msb_']
        self.id_lsb_ = self.val['id_lsb_']
        # Conditions
        self.cond_1 = bool(self.id_msb_ & 0x40000000 != 0)
        self.cond_2 = bool((self.id_msb_ >> 32) & 0xffffffff != 0)
        if self.cond_1:
            self.log2credits = (self.id_msb_ >> 24) & 0x1f
            self.credits = 1 << (self.id_msb_ >> 24) & 0x1f
            self.was_split = bool(self.id_msb_ & 0x80000000)
        if self.cond_2:
            self.locality_id = ((self.id_msb_ >> 32) & 0xffffffff) - 1
        self.msb = self.id_msb_ & 0x7fffff
        self.lsb = self.id_lsb_
        self.has_credit = bool(self.id_msb_ & 0x40000000)
        self.is_locked = bool(self.id_msb_ & 0x20000000)
        self.dont_cache = bool(self.id_msb_ & 0x00800000)

    def to_string(self):
        return "%s: {{ msb=%#02x lsb=%#02x }} %s" % (
            self.type_,
            self.id_msb_,
            self.id_lsb_,
            self.val.address,
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


scimitar.pretty_printers['hpx::naming::gid_type'] = GidTypePrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
