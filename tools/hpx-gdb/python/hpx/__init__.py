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
    # Get the actual type when it points to a reference
    if type_.code in [gdb.TYPE_CODE_REF, gdb.TYPE_CODE_PTR]:
        type_ = type_.target()

    # Get the unqualified type stripped of typedefs.
    type_ = type_.unqualified().strip_typedefs()

    return type_

def pretty_printer_lookup(val):
    type_ = get_basic_type(val.type)
    expr = str(val.type)

    for k, v in printer_dict.iteritems():
        if k.match(expr):
            return v(val)
    return None

def build_printer_dict():
    global printer_dict
    global printer_dict_raw

    include_dicts = lambda m: printer_dict_raw.update(m.printer_dict)

    import backtrace, client_base, future, gid_type, thread_description, thread_state, tuple_

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

def register_hpx_printers(obj=None):
    build_printer_dict()

    if obj == None:
        obj = gdb

    obj.pretty_printers.append(pretty_printer_lookup)

