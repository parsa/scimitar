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

class HPXPrettyPrinterCollection(object):

    class RegexSubprinter(object):
        def __init__(self, name, pattern, printer_type):
            self.name = name
            self.enabled = True
            self.pattern = pattern
            self.printer_type = printer_type
            self.compiled_pattern = re.compile(pattern)

    def __init__(self, name):
        self.name = name
        self.subprinters = None
        self.enabled = True

    def add_printer(self, printer_name, regex_pattern, printer_type):
        if not self.subprinters:
            self.subprinters = []
        self.subprinters.append(self.RegexSubprinter(printer_name, regex_pattern, printer_type))

    def __call__(self, val):
        typename = self.get_basic_type(val.type).tag
        if not typename:
            return None

        for printer in self.subprinters:
            if printer.enabled and printer.compiled_pattern.search(typename):
                return printer.printer_type(val)
        return None

    def get_basic_type(self, type_):
        while (type_.code == gdb.TYPE_CODE_REF or
               type_.code == gdb.TYPE_CODE_TYPEDEF):
            if type_.code == gdb.TYPE_CODE_REF:
                type_ = type_.target()
            else:
                type_ = type_.strip_typedefs()
        return type_.unqualified()
    


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
