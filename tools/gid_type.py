import datetime
import gdb
import re
import sys

class HPXGIDTypePrinter(object):
    "Pretty printer for hpx::naming::gid_type"

    def __init__(self, val):
        self.val = val

    def display_hint(self):
        return 'hpx::naming::gid_type'

    def to_string(self):
        raise Exception('NotImplementedYet')

    def children(self):
        raise Exception('NotImplementedYet')

class HPXIDTypePrinter(object):
    "Pretty printer for hpx::naming::id_type"
    def __init__(self, val):
        self.val = val

    def display_hint(self):
        return 'hpx::naming::id_type'

    def to_string(self):
        raise Exception('NotImplementedYet')

    def children(self):
        raise Exception('NotImplementedYet')

def lookup_function(val):
    lookup_tag = val.type.tag
    if lookup_tag == None:
        return None
    regex = re.compile("^hpx::naming::gid_type$")
    if regex.match(lookup_tag):
        return HPXGIDTypePrinter(val)
    return None
