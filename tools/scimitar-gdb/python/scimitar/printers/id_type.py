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


class IdTypePrinter(object):

    def __init__(self, val, type_):
        self.val = val
        self.type_ = type_
        # Values
        self.px = val['gid_']['px']
        self.id_msb_ = self.px['id_msb_']
        self.id_lsb_ = self.px['id_lsb_']
        self.type_management = self.px['type_']
        self.m_storage = self.px['count_']['value_']['m_storage']

        self.display_string = ''
        self.print_values = []
        # Conditions
        # enum hpx::naming::detail::id_type_management
        #   unknown_deleter = -1
        #   unmanaged = 0
        #   managed = 1
        #   managed_move_credit = 2
        if bool(self.px != 0):
            self.msb = self.id_msb_ & 0x7fffff
            self.lsb = self.id_lsb_

            self.print_values.extend([('msb', '%#02x' % self.msb),
                                      ('lsb', '%#02x' % self.lsb),
                                      ('type', self.type_management), ])

            if bool(self.type_management != 0):
                self.has_credit = bool(self.id_msb_ & 0x40000000)
                self.log2credits = (self.id_msb_ >> 24) & 0x1f
                self.credits = 1 << ((self.id_msb_ >> 24) & 0x1f)
                self.was_split = bool(self.id_msb_ & 0x80000000)

                self.print_values.extend([
                    ('has_credit', self.has_credit),
                    ('log2credits', self.log2credits),
                    ('credits', '%#02x' % self.credits),
                    ('was_split', '%#02x' % self.was_split),
                ])

            self.is_locked = bool(self.id_msb_ & 0x20000000)
            self.dont_cache = bool(self.id_msb_ & 0x00800000)

            self.print_values.extend([('is_locked', self.is_locked),
                                      ('dont_cache', self.dont_cache), ])

            query = ((self.id_msb_ >> 32) & 0xffffffff)
            if bool(query != 0):
                self.locality_id = query - 1
                self.print_values.extend([('locality_id',
                                           self.locality_id, ), ])

            self.print_values.extend([('count',
                                       self.m_storage, ), ])

            self.display_string = "msb=%#02x lsb=%#02x type=%s" % (
                self.id_msb_,
                self.id_lsb_,
                self.type_management,
            )
        else:
            self.display_string = 'empty'

    def to_string(self):
        return "%s: {{ %s }} %s" % (
            self.type_,
            self.display_string,
            self.val.address,
        )

    def children(self):
        return self.print_values


scimitar.pretty_printers['hpx::naming::id_type'] = IdTypePrinter

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
