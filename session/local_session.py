# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from . import manager as _manager
#############################
# mode: local
#############################
def process(cmd, args):
    return (modes.local, None)

class LocalSession():
    def __init__(self, PID):
        pass

