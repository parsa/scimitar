import gdb
import re
import sys
import datetime
import ctypes

class GidTypePrinter(object):
    def __init__(self, val):
        self.val = val

    def display_hint(self):
        return "hpx::naming::gid_type"

    def to_string(self):
        id_msb_ = ctypes.c_long(self.val['id_msb_']).value
        id_lsb_ = ctypes.c_long(self.val['id_msb_']).value
        return "struct hpx::naming::gid_type {{ msb=%#02x lsb=%#02x }}" % (id_msb_, id_lsb_)

    def children(self):
        id_msb_ = ctypes.c_long(self.val['id_msb_']).value
        id_lsb_ = ctypes.c_long(self.val['id_msb_']).value
        subresult = []
        if id_msb_ & 0x40000000:
            subresult.extend([
                ('log2credits', '%s' % str((id_msb_ >> 24) & 0x1f)),
                ('credits', '%s' % str(1 << ((id_msb_ >> 24) & 0x1f))),
                ('was_split', '%s' % str(bool((id_msb_ & 0x80000000)))),
            ])
        return [
            ('msb', '%s' % str(id_msb_ & 0x7fffff)),
            ('lsb', '%s' % str(id_lsb_)),
            ('has_credit', '%s' % str(bool(id_msb_ & 0x40000000))),
            ('is_locked', '%s' % str(bool(id_msb_ & 0x20000000))),
            ('dont_cache', '%s' % str(bool(id_msb_ &  0x00800000))),
            ('locality_id', '%s' % str(((id_msb_ >> 32) & 0xffffffff) - 1)),
        ] + subresult

class IdTypePrinter(object):
    def __init__(self, val):
        self.val = val
        self.gid_ = self.val['gid_']
        self.px = self.gid_['px']

    def display_hint(self):
        return "hpx::naming::id_type"

    def to_string(self):
        if not self.px:
            return "hpx::naming::id_type"
        elif self.px:
            id_msb_ = self.px.dereference()['id_msb_']
            id_lsb_ = self.px.dereference()['id_lsb_']
            return "hpx::naming::id_type {{ msb=%#02x lsb=%#02x }}" % (id_msb_, id_lsb_)
        return None

    def children(self):
        if self.px:
            id_msb_ = ctypes.c_long(self.px.dereference()['id_msb_']).value
            id_lsb_ = ctypes.c_long(self.px.dereference()['id_lsb_']).value
            value_ = str(self.px.dereference()['count_']['value_'])
            type_ = ctypes.c_int(self.px.dereference()['type_']).value
            subresult = []
            if type_ != 0:
                subresult.extend([
                    ('has_credit', str(bool((id_msb_ & 0x40000000)))),
                    ('log2credits', str((id_msb_ >> 24) & 0x1f)),
                    ('credits', str(1 << ((id_msb_ >> 24) & 0x1f))),
                    ('was_split', str(id_msb_ & 0x80000000)),
                ])
            return [
                ('msb', str(id_msb_ & 0x7fffff)),
                ('lsb', str(id_lsb_)),
                ('is_locked', str(id_msb_ & 0x20000000)),
                ('dont_cache', str(id_lsb_ & 0x00800000)),
                ('count', str(value_)),
            ] + subresult
        return []

def lookup_type(val):
    if str(val.type) == 'hpx::naming::gid_type':
        return GidTypePrinter(val)
    elif str(val.type) == 'hpx::naming::id_type':
        return IdTypePrinter(val)
    return None

gdb.pretty_printers.append(lookup_type)


