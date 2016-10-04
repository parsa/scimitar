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

_eval_ = gdb.parse_and_eval


class IdTypePrinter(object):

    def __init__(self, val, type_):
        self.val = val
        self.type_ = type_
        # Values
        self.px = val['gid_']['px']
        self.id_msb_ = self.px['id_msb_']
        self.id_lsb_ = self.px['id_lsb_']
        self.type__ = self.px['type_']
        self.m_storage = self.px['count_']['value_']['m_storage']
        # Conditions
        self.is_px_null = bool(self.px != 0)
        self.is_not_unmanaged = bool(
            _eval_(
                '(%s != hpx::naming::id_type::unmanaged) != 0' %
                (self.type__, )
            )
        )
        self.cond_3 = bool(((self.id_msb_ >> 32) & 0xffffffff) != 0)
        if self.is_px_null:
            self.msb = self.id_msb_ & 0x7fffff
            self.lsb = self.id_lsb_
            self.is_locked = bool(self.id_msb_ & 0x20000000)
            self.dont_cache = bool(self.id_msb_ & 0x00800000)
            if self.is_not_unmanaged:
                self.has_credit = bool(self.id_msb_ & 0x40000000)
                self.log2credits = (self.id_msb_ >> 24) & 0x1f
                self.credits = 1 << ((self.id_msb_ >> 24) & 0x1f)
                self.was_split = bool(self.id_msb_ & 0x80000000)
            if self.cond_3:
                self.locality_id = ((self.id_msb_ >> 32) & 0xffffffff) - 1

    def to_string(self):
        txt = ''
        if self.is_px_null:
            txt = "msb=%#02x lsb=%#02x type=%s" % (
                self.id_msb_,
                self.id_lsb_,
                self.type__,
            )
        else:
            txt = 'empty'
        return "%s: {{ %s }}" % (self.type_, txt, )

    def children(self):
        result = []
        if self.is_px_null:
            if self.is_not_unmanaged:
                result.extend([('has_credit', str(self.has_credit)),
                               ('log2credits', str(self.log2credits)),
                               ('credits', '%#02x' % self.credits),
                               ('was_split', '%#02x' % self.was_split), ])
            if self.cond_3:
                result.extend([('locality_id', str(self.locality_id)), ])
            result.extend([('msb', '%#02x' % self.msb),
                           ('lsb', '%#02x' % self.lsb),
                           ('type', str(self.type__)),
                           ('is_locked', str(self.is_locked)),
                           ('dont_cache', str(self.dont_cache)),
                           ('count', str(self.m_storage)), ])
        return result


scimitar.pretty_printers['hpx::naming::id_type'] = IdTypePrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
