# -*- coding: utf-8 -*-

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

from .apply import apply

_clear_all_chars_attrs           = '\033[0m'
clear_all_chars_attrs            = lambda: apply(_clear_all_chars_attrs)
#
_alternate_intesity_on           = '\033[1m'
alternate_intesity_on            = lambda: apply(_alternate_intesity_on)
#
_alternate_intesity_off          = '\033[22m'
alternate_intesity_off           = lambda: apply(_alternate_intesity_off)
#
_dim                             = '\033[2m'
dim                              = lambda: apply(_dim)
#
_underline_on                    = '\033[4m'
underline_on                     = lambda: apply(_underline_on)
#
_underline_off                   = '\033[24m'
underline_off                    = lambda: apply(_underline_off)
#
_blink_on                        = '\033[5m'
blink_on                         = lambda: apply(_blink_on)
#
_blink_off                       = '\033[25m'
blink_off                        = lambda: apply(_blink_off)
#
_inv_video_on                    = '\033[7m'
inv_video_on                     = lambda: apply(_inv_video_on)
#
_inv_video_off                   = '\033[27m'
inv_video_off                    = lambda: apply(_inv_video_off)
#
_protected_fields_off            = '\033[0}'
protected_fields_off             = lambda: apply(_protected_fields_off)
#
_protected_alt_intensity         = '\033[1}'
protected_alt_intensity          = lambda: apply(_protected_alt_intensity)
#
_protected_underline             = '\033[4}'
protected_underline              = lambda: apply(_protected_underline)
#
_protected_blinking              = '\033[5}'
protected_blinking               = lambda: apply(_protected_blinking)
#
_protected_inverse               = '\033[7}'
protected_inverse                = lambda: apply(_protected_inverse)
#
_protected_all_attrs_off         = '\033[254}'
protected_all_attrs_off          = lambda: apply(_protected_all_attrs_off)
#
_hidden                          = '\033[8m'
hidden                           = lambda: apply(_hidden)

_fg_black                        = '\033[30m'
fg_black                         = lambda: apply(_fg_black)
#
_fg_red                          = '\033[31m'
fg_red                           = lambda: apply(_fg_red)
#
_fg_green                        = '\033[32m'
fg_green                         = lambda: apply(_fg_green)
#
_fg_yellow                       = '\033[33m'
fg_yellow                        = lambda: apply(_fg_yellow)
#
_fg_blue                         = '\033[34m'
fg_blue                          = lambda: apply(_fg_blue)
#
_fg_magenta                      = '\033[35m'
fg_magenta                       = lambda: apply(_fg_magenta)
#
_fg_cyan                         = '\033[36m'
fg_cyan                          = lambda: apply(_fg_cyan)
#
_fg_white                        = '\033[37m'
fg_white                         = lambda: apply(_fg_white)

_bg_black                        = '\033[40m'
bg_black                         = lambda: apply(_bg_black)
#
_bg_red                          = '\033[41m'
bg_red                           = lambda: apply(_bg_red)
#
_bg_green                        = '\033[42m'
bg_green                         = lambda: apply(_bg_green)
#
_bg_yellow                       = '\033[43m'
bg_yellow                        = lambda: apply(_bg_yellow)
#
_bg_blue                         = '\033[44m'
bg_blue                          = lambda: apply(_bg_blue)
#
_bg_magenta                      = '\033[45m'
bg_magenta                       = lambda: apply(_bg_magenta)
#
_bg_cyan                         = '\033[46m'
bg_cyan                          = lambda: apply(_bg_cyan)
#
_bg_white                        = '\033[47m'
bg_white                         = lambda: apply(_bg_white)

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
