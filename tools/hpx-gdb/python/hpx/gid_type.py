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
    def __init__(self, val):
        self.val = val
        self.msb = self.val['id_msb_']
        self.lsb = self.val['id_lsb_']

        self.cond_1 = False
        self.cond_2 = False
        if bool(gdb.parse_and_eval(
            '(%d & 0x40000000ull) != 0' % (self.msb,))
        ):
            self.cond_1 = True
        if bool(gdb.parse_and_eval(
            '((%s >> 32) & 0xffffffffull) != 0' % self.msb)
        ):
            self.cond_2 = True

    def to_string(self):
        return "gid_type: {{ msb=%#02x lsb=%#02x }}" % (
            self.msb,
            self.lsb,
        )

    def children(self):
        result = []
        if self.cond_1:
            result.extend([
                (
                    'log2credits',
                    str(gdb.parse_and_eval(
                        '(%d >> 24) & 0x1full' % (self.msb,)
                    )),
                ),
                (
                    'credits',
                    '%#02x' % gdb.parse_and_eval(
                        '1ull << ((%d >> 24) & 0x1full)' % (self.msb,)
                    ),
                ),
                (
                    'was_split',
                    str(gdb.parse_and_eval(
                        '(%d & 0x80000000ull) ? true : false' % (self.msb,)
                    )),
                ),
            ])
        if self.cond_2:
            result.extend([
                (
                    'locality_id',
                    str(gdb.parse_and_eval(
                        '((%s >> 32) & 0xffffffffull) - 1' % (self.msb,)
                    )),
                ),
            ])
        result.extend([
            (
                'msb',
                '%#02x' % gdb.parse_and_eval(
                    '%s & 0x7fffffull' % (self.msb,))
                ),
            (
                'lsb',
                '%#02x' % gdb.parse_and_eval(
                    '%s' % (self.lsb),
                ),
            ),
            (
                'has_credit',
                '%s' % gdb.parse_and_eval(
                    '(%s & 0x40000000ull) ? true : false' % (self.msb,)
                ),
            ),
            (
                'is_locked',
                '%s' % gdb.parse_and_eval(
                    '(%s & 0x20000000ull) ? true : false' % (self.msb,)
                ),
            ),
            (
                'dont_cache',
                '%s' % gdb.parse_and_eval(
                    '(%s & 0x00800000ull) ? true : false' % (self.msb,)
                ),
            ),
        ])
        return result
printer_dict['hpx::naming::gid_type'] = GidTypePrinter

class IdTypePrinter(object):
    def __init__(self, val):
        self.val = val
        self.px = val['gid_']['px']
        self.msb = self.px['id_msb_']
        self.lsb = self.px['id_lsb_']
        self.type_ = self.px['type_']
        self.m_storage = self.px['count_']['value_']['m_storage']

        self.cond_1 = False
        self.cond_2 = False
        self.cond_3 = False
        if bool(gdb.parse_and_eval('%d != 0' % (self.px,))):
            self.cond_1 = True
            if bool(gdb.parse_and_eval(
                '(%s != hpx::naming::id_type::unmanaged) != 0' % (self.type_,))
            ):
                self.cond_2 = True
            if bool(gdb.parse_and_eval(
                '((%d >> 32) & 0xffffffffull) != 0' % (self.msb,))
            ):
                self.cond_3 = True

    def to_string(self):
        txt = ''
        if bool(gdb.parse_and_eval('%d != 0' % (self.px,))):
            txt = "msb=%#02x lsb=%#02x type=%s" % (
                str(self.msb),
                str(self.lsb),
                str(self.type_),
            )
        else:
            txt = 'empty'
        return "id_type: {{ %s }}" % (txt, )

    def children(self):
        result = []
        if self.cond_1:
            if self.cond_2:
                result.extend([
                    (
                        'has_credit',
                        str(gdb.parse_and_eval(
                            '(%d & 0x40000000ull) ? true : false' % (self.msb,)
                        )),
                    ),
                    (
                        'log2credits',
                        str(gdb.parse_and_eval(
                            '(%d >> 24) & 0x1full' % (self.msb,)
                        )),
                    ),
                    (
                        'credits',
                        '%#02x' % gdb.parse_and_eval(
                            '1ull << ((%d >> 24) & 0x1full)' % (self.msb,)
                        ),
                    ),
                    (
                        'was_split',
                        '%#02x' % gdb.parse_and_eval(
                            '(%d & 0x80000000ull) ? true : false' % (self.msb,)
                        ),
                    ),
                ])
            if self.cond_3:
                result.extend([
                    (
                        'locality_id',
                        '%s' % gdb.parse_and_eval(
                            '((%d >> 32) & 0xffffffffull) - 1' % (self.msb,)
                        ),
                    ),
                ])
            result.extend([
                (
                    'msb',
                    '%#02x' % gdb.parse_and_eval(
                        '%d & 0x7fffffull' % (self.msb,)
                    ),
                ),
                (
                    'lsb',
                    '%#02x' % gdb.parse_and_eval('%d' % (self.lsb,))
                ),
                (
                    'type',
                    '%s' % gdb.parse_and_eval(
                        '%s' % (self.type_,)
                    ),
                ),
                (
                    'is_locked',
                    '%s' % gdb.parse_and_eval(
                        '(%d & 0x20000000ull) ? true : false' % (self.msb,)
                    ),
                ),
                (
                    'dont_cache',
                    '%s' % gdb.parse_and_eval(
                        '(%d & 0x00800000ull) ? true : false' % (self.msb,)
                    ),
                ),
                (
                    'count',
                    '%s' % gdb.parse_and_eval(
                        '%s' % (self.m_storage,)
                    ),
                ),
            ])
        return result
printer_dict['hpx::naming::id_type'] = IdTypePrinter

