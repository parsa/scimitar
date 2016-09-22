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

class GidTypePrinter(object):
    def __init__(self, expr, val):
        self.val = val
        self.expr = expr

    def display_hint(self):
        return self.expr

    def to_string(self):
        return "(%s) {{ msb=%#02x lsb=%#02x }} %#02x" % (
            self.expr,
            gdb.parse_and_eval('id_msb_'),
            gdb.parse_and_eval('id_lsb_'),
            self.val.address,
        )

    def children(self):
        result = []
        if bool(gdb.parse_and_eval('(id_msb_ & 0x40000000ull) != 0')):
            result.extend([
                ('log2credits', '%s' % gdb.parse_and_eval('(id_msb_ >> 24) & 0x1full')),
                ('credits', '%#02x' % gdb.parse_and_eval('1ull << ((id_msb_ >> 24) & 0x1full)')),
                ('was_split', '%s' % gdb.parse_and_eval('(id_msb_ & 0x80000000ull) ? true : false')),
            ])
        if bool(gdb.parse_and_eval('((id_msb_ >> 32) & 0xffffffffull) != 0')):
            result.extend([
                ('locality_id', '%s' % gdb.parse_and_eval('((id_msb_ >> 32) & 0xffffffffull) - 1')),
            ])
        result.extend([
            ('msb', '%#02x' % gdb.parse_and_eval('id_msb_ & 0x7fffffull')),
            ('lsb', '%#02x' % gdb.parse_and_eval('id_lsb_')),
            ('has_credit', '%s' % gdb.parse_and_eval('(id_msb_ & 0x40000000ull) ? true : false')),
            ('is_locked', '%s' % gdb.parse_and_eval('(id_msb_ & 0x20000000ull) ? true : false')),
            ('dont_cache', '%s' % gdb.parse_and_eval('(id_msb_ & 0x00800000ull) ? true : false')),
        ])
        return result
printer_dict['hpx::naming::gid_type'] = GidTypePrinter

class IdTypePrinter(object):
    def __init__(self, expr, val):
        self.val = val
        self.expr = expr

    def display_hint(self):
        return self.expr

    def to_string(self):
        txt = ''
        if bool(gdb.parse_and_eval('gid_.px != 0')):
            txt = "{{ msb=%#02x lsb=%#02x type=%s }}" % (
                gdb.parse_and_eval('gid_.px->id_msb_'),
                gdb.parse_and_eval('gid_.px->id_lsb_'),
                gdb.parse_and_eval('gid_.px->type_'),
            )
        if bool(gdb.parse_and_eval('gid_.px == 0')):
            txt = 'empty'
        return "(%s) %s %#02x" % (self.expr, txt, self.val.address)

    def children(self):
        result = []
        if bool(gdb.parse_and_eval('gid_.px != 0')):
            if bool(gdb.parse_and_eval('(gid_.px->type_ != unmanaged) != 0')):
                result.extend([
                    ('has_credit', '%s' % gdb.parse_and_eval('(gid_.px->id_msb_ & 0x40000000ull) ? true : false')),
                    ('log2credits', '%s' % gdb.parse_and_eval('(gid_.px->id_msb_ >> 24) & 0x1full')),
                    ('credits', '%#02x' % gdb.parse_and_eval('1ull << ((gid_.px->id_msb_ >> 24) & 0x1full)')),
                    ('was_split', '%#02x' % gdb.parse_and_eval('(gid_.px->id_msb_ & 0x80000000ull) ? true : false')),
                ])
            if bool(gdb.parse_and_eval('((gid_.px->id_msb_ >> 32) & 0xffffffffull) != 0')):
                result.extend([
                    ('locality_id', '%s' % gdb.parse_and_eval('((gid_.px->id_msb_ >> 32) & 0xffffffffull) - 1')),
                ])
            result.extend([
                ('msb', '%#02x' % gdb.parse_and_eval('gid_.px->id_msb_ & 0x7fffffull')),
                ('lsb', '%#02x' % gdb.parse_and_eval('gid_.px->id_lsb_')),
                ('type', '%s' % gdb.parse_and_eval('gid_.px->type_')),
                ('is_locked', '%s' % gdb.parse_and_eval('(gid_.px->id_msb_ & 0x20000000ull) ? true : false')),
                ('dont_cache', '%s' % gdb.parse_and_eval('(gid_.px->id_msb_ & 0x00800000ull) ? true : false')),
                ('count', '%s' % gdb.parse_and_eval('gid_.px->count_.value_')),
            ])
        return result
printer_dict['hpx::naming::id_type'] = IdTypePrinter
