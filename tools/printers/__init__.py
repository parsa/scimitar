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
import re

printer_dict = {}
printer_dict_raw = {}

def get_basic_type(type_):
    # If it points to a reference, get the reference.
    if type_.code == gdb.TYPE_CODE_REF:
        type_ = type_.target()

    #if type_.code == gdb.TYPE_CODE_PTR:
    #    type_ = type.dereference()

    # Get the unqualified type stripped of typedefs.
    type_ = type_.unqualified().strip_typedefs()

    return type_

def lookup_printer(val):
    raw_type_ = val.type
    type_ = get_basic_type(raw_type_)

    type_ = type_.unqualified().strip_typedefs()

    expr = str(raw_type_)
    for k, v in printer_dict.iteritems():
        pass
        m = k.match(expr)
        if m:
            tmpl = None
            try:
                tmpl = m.group('tmpl')
            except IndexError:
                pass
            if tmpl:
                return v(expr, val, tmpl)
            return v(expr, val)
            
    return None

def build_printer_dict():
    global printer_dict
    global printer_dict_raw

    import backtrace, client_base, future, gid_type, thread_description, thread_state, tuple_
    include_dicts = lambda m: printer_dict_raw.update(m.printer_dict)

    include_dicts(backtrace)
    include_dicts(client_base)
    include_dicts(future)
    include_dicts(gid_type)
    include_dicts(thread_description)
    include_dicts(thread_state)
    include_dicts(tuple_)

    for k, v in printer_dict_raw.iteritems():
        pattern = re.compile('^(const )?%s( \*)?( const)?$' % k)
        printer_dict[pattern] = v

build_printer_dict()
gdb.pretty_printers.append(lookup_printer)

