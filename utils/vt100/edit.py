# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from sys import stdout as o

_erase_right                     = '\033[K'
_erase_left                      = '\033[1K'
_erase_line                      = '\033[2K'
_erase_down                      = '\033[J'
_erase_up                        = '\033[1J'

def erase_right():
    o.write(_erase_right)
def erase_left():
    o.write(_erase_left)
def erase_line():
    o.write(_erase_line)
def erase_down():
    o.write(_erase_down)
def erase_up():
    o.write(_erase_up)

_clear_screen                    = '\033[2J'
def clear_screen():
    o.write(_clear_screen)

_insert_mode                     = '\033[4h'
_replace_mode                    = '\033[4l'

def insert_mode():
    o.write(_insert_mode)
def replace_mode():
    o.write(_replace_mode)


def _delete_right(count=1):
    return '\033[{COUNT}P'.format(COUNT=count)
def delete_right(count=1):
    o.write(_delete_lines(count))

def _delete_left(count=1):
    return '\033[{COUNT}M'.format(COUNT=count)
def delete_left(count=1):
    o.write(_delete_left(count))

def _delete_lines(count=1):
    return '\033{COUNT}L'.format(COUNT=count)
def delete_lines(count=1):
    o.write(_delete_lines(count))
