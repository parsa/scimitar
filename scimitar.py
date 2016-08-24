#!/usr/bin/env python3
# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import signal
from sys import stdout
import time
import _thread
import threading
import utils
from utils import config
import session

# Constants
BANNER = '''Scimitar (Alpha) 0.3.193 build 3097
Copyright (C) 2016 Parsa Amini
Copyright (C) 2016 Hartmut Kaiser
Copyright (C) 2016 Thomas Heller
Be licensed under Boost Software License, Version 1.0
<http://www.boost.org/LICENSE_1_0.txt>
'tis be free software; ye be free to change 'n redistribute it. Thar be NO
warranty; not even for MERCHANTABILITY or FITNESS FER A PARTICULAR PURPOSE.
'''

# HACK: Test async output printing
def noise():
    pass
    #utils.print_ahead('Noise.', config.settings['ui']['prompt'])
#    for i in range(20):
#        time.sleep(4)
#
#        utils.print_ahead('Noise.', config.settings['ui']['prompt'])

# Dispatch the command and its arguments to the appropriate mode's processor
command_switcher = {
    session.modes.offline: session.offline.process,
    session.modes.local: session.local.process,
    session.modes.remote: session.remote.process,
}

def main():
    # Clear the terminal
    utils.vt100.terminal.reset()
    # Ahoy
    utils.print_out(BANNER)

    # Initial session mode
    state = session.modes.offline

    # Async output printing
    _thread.start_new_thread(noise, ())

    while state != session.modes.quit:
        # FIXME: This is a blocking call. Have found no way to avoid it when readline is added to the equation
        user_input = utils.raw_input_async(config.settings['ui']['prompt'])
        utils.print_out(str(user_input.encode('unicode_escape'), 'ascii') if user_input else '')

        if user_input:
            parts = user_input.split()
            cmd = parts[0]
            args = parts[1:]

            # Run the appropriate mode's processing function
            command_fn = command_switcher.get(state)

            try:
                state, update_msg = command_fn(cmd, args)
                print('update_msg:', update_msg)
                if update_msg:
                    utils.print_out(update_msg)
            except session.UnknownCommandException as e:
                utils.print_out('Unknown command: {}'.format(e.expression))
            except session.BadArgsException as e:
                utils.print_out('Command "{0}" cannot be initiated with the arguments provided. {1}'.format(e.expression, e.message))
            except session.BadConfigException as e:
                utils.print_out('The command encountered errors with the provided arguments. {0}: {1}.'.format(e.expression, e.message))
            except session.CommandFailedException as e:
                utils.print_out('The command encountered an error and did not run properly. {0}: {1}.'.format(e.expression, e.message))

if __name__ == '__main__':
    # NOTE: Multiple SIGKILLs required to force close.
    utils.raw_input_async.last_kill_sig = None

    main()
