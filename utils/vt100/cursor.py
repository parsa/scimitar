# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from sys import stdout as o

def up(count=1):
    return '\x1b[{COUNT}A'.format(COUNT=count)

def down(count=1):
    return '\033[{COUNT}B'.format(COUNT=count)

def forward(count=1):
    return '\033[{COUNT}C'.format(COUNT=count)

def backward(count=1):
    return '\033[{COUNT}D'.format(COUNT=count)

def column(column_id=0):
    return '\033[{COL}G'.format(COL=column_id)

def set_cursor(row, column):
    return '\033[{ROW};{COLUMN}f'.format(ROW=row, COLUMN=column)

_save_cursor                    = '\033[s'
_unsave_cursor                  = '\033]s'
_save_cursor_attr               = '\0337'
_restore_cursor_attr            = '\0338'

def save_cursor():
    o.write(_save_cursor)
def unsave_cursor():
    o.write(_unsave_cursor)
def save_cursor_attr():
    o.write(_save_cursor_attr)
def restore_cursor_attr():
    o.write(_restore_cursor_attr)

_cursor_off                     = '\033[?25l'
_cursor_on                      = '\033[?25h'

def cursor_on():
    o.write(_cursor_on)
def cursor_off():
    o.write(_cursor_off)

_top_left                       = '\033[H'
def top_left():
    o.write(_top_left)

lf                              = '\033D' # '\033[20h'
cr_lf                           = '\033E'
inv_lf                          = '\033M' # '\033I'
