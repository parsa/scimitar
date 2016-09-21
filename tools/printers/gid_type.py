import gdb
import re
import sys
import datetime
import ctypes

class GidTypePrinter(object):
    def __init__(self, val):
        self.val = val
        self.id_msb_ = ctypes.c_long(self.val['id_msb_']).value
        self.id_lsb_ = ctypes.c_long(self.val['id_msb_']).value

    def display_hint(self):
        return "hpx::naming::gid_type"

    def to_string(self):
        id_msb_ = ctypes.c_long(self.val['id_msb_']).value
        id_lsb_ = ctypes.c_long(self.val['id_msb_']).value
        return "struct hpx::naming::gid_type {{ msb=%#02x lsb=%#02x }} %#02x" % (id_msb_, id_lsb_, self.val.address)

    def children(self):
        result = []
        if id_msb_ & 0x40000000:
            result.extend([
                ('log2credits', '%s' % str((self.id_msb_ >> 24) & 0x1f)),
                ('credits', '%s' % str(1 << ((self.id_msb_ >> 24) & 0x1f))),
                ('was_split', '%s' % str(bool((self.id_msb_ & 0x80000000)))),
            ])
        if ((id_msb_ >> 32) & 0xffffffff):
            result.extend([
                ('locality_id', '%s' % str(((self.id_msb_ >> 32) & 0xffffffff) - 1)),
            ])
        result.extend([
            ('msb', '%s' % str(self.id_msb_ & 0x7fffff)),
            ('lsb', '%s' % str(self.id_lsb_)),
            ('has_credit', '%s' % str(bool(self.id_msb_ & 0x40000000))),
            ('is_locked', '%s' % str(bool(self.id_msb_ & 0x20000000))),
            ('dont_cache', '%s' % str(bool(self.id_msb_ &  0x00800000))),
        ])
        return result

class IdTypePrinter(object):
    def __init__(self, val):
        self.val = val
        self.gid_ = self.val['gid_']
        self.Ppx = self.val['gid_']['px']
        self.id_type_management_enum = {
            -1: 'hpx::naming::detail::unknown_deleter',
            0: 'hpx::naming::detail::unmanaged',
            1: 'hpx::naming::detail::managed',
            2: 'hpx::naming::detail::managed_move_credit',
        }

    def display_hint(self):
        return "hpx::naming::id_type"

    def to_string(self):
        txt = ''
        if self.Ppx:
            px = self.Ppx.dereference()
            id_msb_ = px['id_msb_']
            id_lsb_ = px['id_lsb_']
            type_ = ctypes.c_int(px['type_']).value
            str_type_ = self.id_type_management_enum.get(type_, 'None')
            txt = "{{ msb=%#02x lsb=%#02x type=%s }}" % (id_msb_, id_lsb_, str_type_)
        return "(hpx::naming::id_type) %s %#02x" % (txt, self.val.address)

    def children(self):
        if self.Ppx:
            px = self.Ppx.dereference()
            id_msb_ = ctypes.c_long(px['id_msb_']).value
            id_lsb_ = ctypes.c_long(px['id_lsb_']).value
            value_ = str(px['count_']['value_'])
            type_ = ctypes.c_int(px['type_']).value
            str_type_ = self.id_type_management_enum.get(type_, 'None')
            result = []
            if str_type_ != 'hpx::naming::detail::unmanaged':
                result.extend([
                    ('has_credit', str(bool((id_msb_ & 0x40000000)))),
                    ('log2credits', str((id_msb_ >> 24) & 0x1f)),
                    ('credits', str(hex(1 << ((id_msb_ >> 24) & 0x1f)))),
                    ('was_split', str(bool(id_msb_ & 0x80000000))),
                ])
            if ((id_msb_ >> 32) & 0xffffffff):
                result.extend([
                    ('locality_id', ((id_msb_ >> 32) & 0xffffffff) - 1),
                ])
            result.extend([
                ('type', str_type_),
                ('msb', str(id_msb_ & 0x7fffff)),
                ('lsb', str(id_lsb_)),
                ('is_locked', str(bool(id_msb_ & 0x20000000))),
                ('dont_cache', str(bool(id_lsb_ & 0x00800000))),
                ('count', str(value_)),
            ])
            return result
        return []

def lookup_type(val):
    type_ = val.type

    if type_.code == gdb.TYPE_CODE_REF:
        type_ = type.dereference()

    type_ = type_.unqualified().strip_typedefs()

    expr = str(type_)
    if re.match('^(const )?hpx::naming::gid_type?( const)?$', expr):
        return GidTypePrinter(val)
    elif re.match('^(const )?hpx::naming::id_type( \*)?( const)?$', expr):
        return IdTypePrinter(val)
    return None

gdb.pretty_printers.append(lookup_type)

