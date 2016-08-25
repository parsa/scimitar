# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

class UnknownCommandError(Exception):
    '''Raised when the command called does not exist.'''

    def __init__(self, cmd):
        self.message = 'Unknown command entered'
        self.expression = cmd

class BadArgsError(Exception):
    '''Raised when arguments of a command are nonsense.'''
    def __init__(self, cmd, expectation):
        self.message = expectation
        self.expression = cmd

class CommandFailedError(Exception):
    '''Raised when command fails and no clue what's wrong.'''
    def __init__(self, cmd, expectation):
        self.message = expectation
        self.expression = cmd

class BadConfigError(Exception):
    '''Raised when configuration seems to have wrong values.'''
    def __init__(self, cmd, expectation):
        self.message = expectation
        self.expression = cmd

class TimeOutError(Exception):
    '''Can be raised when something times out.'''
    pass

class UnexpectedResponseError(Exception):
    '''Raised when encountering an unexpected response during SSH connections.'''
    pass

class NoRunningAppFoundError(Exception):
    '''Raised when no running application is found on the system'''
    pass

class CommandImplementationIncompleteError(Exception):
    '''Raised when a command I had to remove is called.'''
    pass


