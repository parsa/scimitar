# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from sys import stdout as o

_lock_keyboard                   = '\033[2h'
_unlock_keyboard                 = '\033[2l'

def lock_keyboard():
    o.write(_lock_keyboard)
def unlock_keyboard():
    o.write(_unlock_keyboard)

_auto_repeat_on                  = '\033[8h'
_auto_repeat_off                 = '\033[8l'

def auto_repeat_on():
    o.write(_auto_repeat_on)
def auto_repeat_off():
    o.write(_auto_repeat_off)

_lights_off_on_keyboard          = '\033[0q'
def lights_off_on_keyboard():
    o.write(_lights_off_on_keyboard)
