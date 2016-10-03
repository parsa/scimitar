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
'''
This module provides compatibility with older GDB versions that do not
have gdb.printing available.
'''
import gdb
import re


class HPXSubprinter(object):

    def __init__(self, name, printer_type):
        self.name = name
        self.printer_type = printer_type
        self.enabled = True

    def invoke(self, val):
        return self.printer_type(val)


class PrinterLookup():

    def __init__(self):
        self.mappings = {}

    def add_type(self, regex_pattern, printer):
        compiled_pattern = re.compile(regex_pattern)
        self.mappings[compiled_pattern] = printer

    def __len__(self):
        return len(self.mappings)

    def __iter__(self):
        return self.mappings

    def __getitem__(self, type):
        typename = self._basic_type(type)
        if typename:
            for i in self.mappings.keys():
                if i.match(typename):
                    return self.mappings[i]
        return None

    def _basic_type(self, type):
        basic_type = self.basic_type(type)
        return basic_type

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
        self.lookup = PrinterLookup()
        self.enabled = True

    def add_printer(self, printer_name, regex_pattern, printer_type):
        printer = HPXSubprinter(printer_name, printer_type)
        self.subprinters.append(printer)
        self.lookup.add_type(regex_pattern, printer)

    def __call__(self, val):
        printer = self.lookup[val.type]
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
