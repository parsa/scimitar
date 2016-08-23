#!/usr/bin/env python

# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import os
import urllib2

url = 'https://raw.githubusercontent.com/STEllAR-GROUP/hpx/master/tools/gdb/hpx.py'
response = urllib2.urlopen(url)
code = response.read()

with open('threads.py', 'wb') as file:
    file.write(code)
#os.system('bash threads.py')
