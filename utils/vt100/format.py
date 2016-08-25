# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from sys import stdout as o

_clear_all_chars_attrs           = '\033[0m'
def clear_all_chars_attrs():
    o.write(_clear_all_chars_attrs)

alternate_intesity_on           = '\033[1m'
alternate_intesity_off          = '\033[22m'
dim                             = '\033[2m'
underline_on                    = '\033[4m'
underline_off                   = '\033[24m'
blink_on                        = '\033[5m'
blink_off                       = '\033[25m'
inv_video_on                    = '\033[7m'
inv_video_off                   = '\033[27m'
hidden                          = '\033[8m'

fg_black                        = '\033[30m'
fg_red                          = '\033[31m'
fg_green                        = '\033[32m'
fg_yellow                       = '\033[33m'
fg_blue                         = '\033[34m'
fg_magenta                      = '\033[35m'
fg_cyan                         = '\033[36m'
fg_white                        = '\033[37m'

bg_black                        = '\033[40m'
bg_red                          = '\033[41m'
bg_green                        = '\033[42m'
bg_yellow                       = '\033[43m'
bg_blue                         = '\033[44m'
bg_magenta                      = '\033[45m'
bg_cyan                         = '\033[46m'
bg_white                        = '\033[47m'
