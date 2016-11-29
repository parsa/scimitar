#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Scimitar: Ye Distributed Debugger
# 
# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#
import signal
from sys import stdout
import time
import thread
import threading

from util import vt100, print_out, print_ahead, print_error, raw_input_async, repr_str, cleanup_terminal, init_terminal, register_completer
from __ver__ import VERSION
from sessions import modes, offline_session, debug_session
import config
import errors

# Constants
BANNER = '''
                                                                          7?$7: 
   ____       _           _ _                                          +DDO7I~+.
  / ___|  ___(_)_ __ ___ (_) |_ __ _ _ __                    .I:    .NDDOZ?. ...
  \___ \ / __| | '_ ` _ \| | __/ _` | '__|                    .+~  DDD8Z+.      
   ___) | (__| | | | | | | | || (_| | |                       .7?IDD8Z+.        
  |____/ \___|_|_| |_| |_|_|\__\__,_|_|   (alpha)            .$?I+=$=.          
                                                          .?77$=+..?.           
            {get_version_result}                        .III77777,.:I.          
                                                     .~?????I,?.    .~.         
                                                  ..?++++?=?+.                  
                                                .?+++++I 7:                     
                                             .+????+I.$+.                       
                                          .+?????I,7+.                          
                                    ..:=+++++?I:7=.                             
+.                       .       ,~~~===++++,$=.                                
 .:77$7777I?~~++=?IIII?++++=====~~~~~~=~.$?,                                    
    .=777777III????????+++?=:?~=~~,.?I~..                                       
        ,+77I????++++++=+++=,,I7+:.                                             
           . ..,:~====~::,.                                                     

Copyright (C) 2016 Parsa Amini
Copyright (C) 2016 Hartmut Kaiser
Copyright (C) 2016 Thomas Heller

Be licensed under Boost Software License, Version 1.0
<http://www.boost.org/LICENSE_1_0.txt>
'tis be free software; ye be free to change 'n redistribute it. Thar be NO
warranty; not even for MERCHANTABILITY or FITNESS FER A PARTICULAR PURPOSE.
'''.format(get_version_result = VERSION.rjust(20))


# HACK: Test async output printing
def noise():
    pass
    #print_ahead('Noise.', config.settings['ui']['prompt'])
#    for _ in range(20):
#        time.sleep(4)
#
#        print_ahead('Noise.', config.settings['ui']['prompt'])

# Dispatch the command and its arguments to the appropriate mode's processor


completer_switcher = {
    modes.offline: offline_session.OfflineSessionCommandCompleter().complete,
    modes.debugging: debug_session.DebugSessionCommandCompleter().complete,
    modes.quit: None,
}

command_handler_switcher = {
    modes.offline: offline_session.process,
    modes.debugging: debug_session.process,
}


def main():
    try:
        # NOTE: Multiple SIGKILLs required to force close.
        raw_input_async.last_kill_sig = None

        # Clear the terminal
        vt100.terminal.reset()

        # Ahoy
        print_out(BANNER)

        # Initial session mode
        current_mode = modes.offline

        # Init terminal
        init_terminal()
        register_completer(completer_switcher[current_mode])

        # Async output printing
        thread.start_new_thread(noise, ())

        prompts_list = config.settings['ui']['prompts']
        get_prompt = lambda: {
            modes.offline: prompts_list[0],
            modes.debugging: prompts_list[1]
        }[current_mode]

        # Main loop
        while current_mode != modes.quit:
            vt100.unlock_keyboard()
            # FIXME: raw_input_async still is a blocking call. Have found no way to
            # avoid it. Reason: readline initiates a system call that I have no
            # clue to get out of.
            user_input, key_seq = raw_input_async(get_prompt())
            # HACK: Temporarily disabled for debugging
            #vt100.lock_keyboard()
            ## HACK: Display the user's input
            #print_out(user_input.encode('string_escape') if user_input else '')

            # An empty string is a valid empty
            # If the input was a control signal split might just remove it
            packed_input = user_input if user_input else key_seq
            if not packed_input:
                continue
            cmd, args = packed_input[0], packed_input[1:]
            # Run the appropriate mode's processing function
            cmd_processor_fn = command_handler_switcher.get(current_mode)

            try:
                current_mode, update_msg = cmd_processor_fn(cmd, args)
                register_completer(completer_switcher[current_mode])

                if update_msg:
                    print_out(update_msg)
            except errors.UnknownCommandError as e:
                print_error(
                    'Unknown command: {u1}{cmd}{u0}',
                    cmd = repr_str(e.expression)
                )
            except errors.BadArgsError as e:
                print_error(
                    'Command "{u1}{cmd}{u0}" cannot be initiated with the arguments provided.\n{msg}',
                    cmd = e.expression,
                    msg = e.message
                )
            except errors.BadConfigError as e:
                print_error(
                    'The command encountered errors with the provided arguments.\n{u1}{cmd}{u0}: {msg}',
                    cmd = e.expression,
                    msg = e.message
                )
            except errors.CommandFailedError as e:
                print_error(
                    'The command encountered an error and did not run properly.\n{u1}{cmd}{u0}: {msg}',
                    cmd = e.expression,
                    msg = e.message
                )
            except errors.CommandImplementationIncompleteError:
                print_error(
                    'The implementation of command "{u1}{cmd}{u0}" is not complete yet.',
                    cmd = cmd
                )
            except KeyboardInterrupt:
                print_error('Action cancelled by the user.')
    finally:
        cleanup_terminal()


if __name__ == '__main__':
    main()

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
