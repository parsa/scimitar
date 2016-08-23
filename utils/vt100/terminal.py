# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from sys import stdout as o

_reset                           = '\033c'
def reset():
    o.write(_reset)
#soft_reset                      = '\033[!p'
_fill_screen_with_E              = '\033#8'
def fill_screen_with_E():
    o.write(_fill_screen_with_E)

_enable_line_wrap                = '\033[7h'
_disable_line_wrap               = '\033[7l'

def enable_line_wrap():
    o.write(_enable_line_wrap)
def disable_line_wrap():
    o.write(_disable_line_wrap)
