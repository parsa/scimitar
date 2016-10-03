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
import re
from collections import Mapping


class HPXSubprinter(object):

    def __init__(self, name, printer_type):
        self.name = name
        self.printer_type = printer_type
        self.enabled = True

    def invoke(self, val):
        return self.printer_type(self.name, val)


class NameLookup(Mapping):

    def __init__(self):
        self.map = {}
        #self.name_regex = re.compile('^([\w:]+)(<.*>)?')

    def add_type(self, regex_pattern, printer):
        compiled_pattern = re.compile(regex_pattern)
        self.map[compiled_pattern] = printer

    def __len__(self):
        return len(self.map)

    def __getitem__(self, type):
        typename = self._basic_type(type)
        if typename:
            for i in self.map.keys():
                if i.match(typename):
                    return self.map[i]
            #if typename and typename in self.map:
            #    return self.map[typename]
        return None

    def __iter__(self):
        return self.map

    def _basic_type(self, type):
        basic_type = self.basic_type(type)
        return basic_type
        #if basic_type:
        #    match = self.name_regex.match(basic_type)
        #    if match:
        #        return match.group(1)
        #return None

    @staticmethod
    def basic_type(type):
        if type.code == gdb.TYPE_CODE_REF:
            type = type.target()
        type = type.unqualified().strip_typedefs()
        return type.tag


class HPXPrinterCollection(object):

    def __init__(self, name):
        self.name = name
        self.subprinters = []
        self.name_lookup = NameLookup()
        self.enabled = True

    def add_printer(self, printer_name, regex_pattern, printer_type):
        printer = HPXSubprinter(printer_name, printer_type)
        self.subprinters.append(printer)
        self.name_lookup.add_type(regex_pattern, printer)

    def __call__(self, val):
        printer = self.name_lookup[val.type]
        if printer:
            return printer.invoke(val)
        return None


def register_pretty_printer(obj, printer):

    if use_gdb_printing:
        gdb.printing.register_pretty_printer(obj, printer)
    else:
        if obj is None:
            obj = gdb
        obj.pretty_printers.append(printer)


use_gdb_printing = True
try:
    import gdb.printing
except ImportError:
    use_gdb_printing = False

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
