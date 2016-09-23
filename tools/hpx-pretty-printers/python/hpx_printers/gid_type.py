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
            self.val['id_msb_'],
            self.val['id_lsb_'],
            self.val.address,
        )

    def children(self):
        result = []
        if bool(gdb.parse_and_eval('(%d & 0x40000000ull) != 0' % (self.val['id_msb_'],))):
            result.extend([
                ('log2credits', '%s' % gdb.parse_and_eval('(%d >> 24) & 0x1full' % (self.val['id_msb_'],))),
                ('credits', '%#02x' % gdb.parse_and_eval('1ull << ((%d >> 24) & 0x1full)' % (self.val['id_msb_'],))),
                ('was_split', '%s' % gdb.parse_and_eval('(%d & 0x80000000ull) ? true : false' % (self.val['id_msb_'],))),
            ])
        if bool(gdb.parse_and_eval('((%s >> 32) & 0xffffffffull) != 0' % self.val['id_msb_'])):
            result.extend([
                ('locality_id', '%s' % gdb.parse_and_eval('((%s >> 32) & 0xffffffffull) - 1' % (self.val['id_msb_'],))),
            ])
        result.extend([
            ('msb', '%#02x' % gdb.parse_and_eval('%s & 0x7fffffull' % (self.val['id_msb_'],))),
            ('lsb', '%#02x' % gdb.parse_and_eval('%s' % (self.val['id_lsb_']),)),
            ('has_credit', '%s' % gdb.parse_and_eval('(%s & 0x40000000ull) ? true : false' % (self.val['id_msb_'],))),
            ('is_locked', '%s' % gdb.parse_and_eval('(%s & 0x20000000ull) ? true : false' % (self.val['id_msb_'],))),
            ('dont_cache', '%s' % gdb.parse_and_eval('(%s & 0x00800000ull) ? true : false' % (self.val['id_msb_'],))),
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
        if bool(gdb.parse_and_eval('%d != 0' % (self.val['gid_']['px'],))):
            txt = "{{ msb=%#02x lsb=%#02x type=%s }}" % (
                gdb.parse_and_eval('%s' % (self.val['gid_']['px']['id_msb_'],)),
                gdb.parse_and_eval('%s' % (self.val['gid_']['px']['id_lsb_'],)),
                gdb.parse_and_eval('%s' % (self.val['gid_']['px']['type_'],)),
            )
        else:
            txt = 'empty'
        return "(%s) %s %#02x" % (self.expr, txt, self.val.address)

    def children(self):
        result = []
        if bool(gdb.parse_and_eval('%d != 0' % (self.val['gid_']['px'],))):
            if bool(gdb.parse_and_eval('(%s != hpx::naming::id_type::unmanaged) != 0' % (self.val['gid_']['px']['type_'],))):
                result.extend([
                    ('has_credit', '%s' % gdb.parse_and_eval('(%d & 0x40000000ull) ? true : false' % (self.val['gid_']['px']['id_msb_'],))),
                    ('log2credits', '%s' % gdb.parse_and_eval('(%d >> 24) & 0x1full' % (self.val['gid_']['px']['id_msb_'],))),
                    ('credits', '%#02x' % gdb.parse_and_eval('1ull << ((%d >> 24) & 0x1full)' % (self.val['gid_']['px']['id_msb_'],))),
                    ('was_split', '%#02x' % gdb.parse_and_eval('(%d & 0x80000000ull) ? true : false' % (self.val['gid_']['px']['id_msb_'],))),
                ])
            if bool(gdb.parse_and_eval('((%d >> 32) & 0xffffffffull) != 0' % (self.val['gid_']['px']['id_msb_'],))):
                result.extend([
                    ('locality_id', '%s' % gdb.parse_and_eval('((%d >> 32) & 0xffffffffull) - 1' % (self.val['gid_']['px']['id_msb_'],))),
                ])
            result.extend([
                ('msb', '%#02x' % gdb.parse_and_eval('%d & 0x7fffffull' % (self.val['gid_']['px']['id_msb_'],))),
                ('lsb', '%#02x' % gdb.parse_and_eval('%d' % (self.val['gid_']['px']['id_lsb_'],))),
                ('type', '%s' % gdb.parse_and_eval('%s' % (self.val['gid_']['px']['type_'],))),
                ('is_locked', '%s' % gdb.parse_and_eval('(%d & 0x20000000ull) ? true : false' % (self.val['gid_']['px']['id_msb_'],))),
                ('dont_cache', '%s' % gdb.parse_and_eval('(%d & 0x00800000ull) ? true : false' % (self.val['gid_']['px']['id_msb_'],))),
                ('count', '%s' % gdb.parse_and_eval('%s' % (self.val['gid_']['px']['count_']['value_']['m_storage'],))),
            ])
        return result
printer_dict['hpx::naming::id_type'] = IdTypePrinter

