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

hpx_threads_available = False

def main():
    import os
    import urllib2

    url = 'https://raw.githubusercontent.com/STEllAR-GROUP/hpx/master/tools/gdb/hpx.py'
    response = urllib2.urlopen(url)
    code = response.read()

    with open('hpx_threads.py', 'wb') as file:
        file.write(code)
    #os.system('bash threads.py')

if __name__ == '__main__':
    main()