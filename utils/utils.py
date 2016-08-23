# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from . import vt100
from . import config
from sys import stdout, exit
from datetime import datetime as time
import signal
import readline
import re
import select

def print_ahead(expr, prompt=''):
    current_input = readline.get_line_buffer()
    vt100.edit.erase_line()
    stdout.write('\r')

    print(expr)
    stdout.write(prompt + current_input)
    stdout.flush()

def print_out(expr):
    stdout.write(expr + '\n')
    stdout.flush()

class AlarmException(Exception):
    pass

def __alarm_handler(signum, frame):
    raise AlarmException

class StopException(Exception):
    pass

def __stop_handler(signum, frame):
    raise StopException

class QuitException(Exception):
    pass

def __quit_handler(signum, frame):
    raise QuitException

def stream_readline(stream):
    return str(stream.readline(), 'ascii')

def stream_writeline(msg, stream):
    stream.write(bytes(msg, 'ascii'))
    stream.flush()
    
def attempt_read(stream, retries=-1, timeout=-1, pattern=None):
    """Tries to read until a condition is met.
    Returns empty if nothing was read."""
    before_read = time.now()

    is_ready = select.poll()
    is_ready.register(stream, select.POLLIN)

    out_text = ''
    q = 0
    while True:
        if timeout > 0 and (time.now() - before_read).seconds >= timeout:
            break

        if not is_ready.poll(0):
            q += 1
            if retries > 0 and q >= retries:
                break
            else:
                continue

        if pattern and re.search(pattern, out_text):
            break

        out_text += stream_readline(stream)
    return out_text

# MERGE: asyncio_processing_loop (939bad3d2718407e8b07176c14839ba0)
def raw_input_async(prompt='', timeout=5):
    """This is a blocking user input read function.
    It has to be running inside the main thread because it contains code handling signals.
    Despite what the title suggests this version IS NOT ASYNC.
    ALARM signal is not enabled."""
    #signal.signal(signal.SIGINT, signal_handler) # <C-c>
    signal.signal(signal.SIGTSTP, __stop_handler) # <C-z>
    signal.signal(signal.SIGQUIT, __quit_handler) # <C-\>
    #signal.signal(signal.SIGALRM, __alarm_handler)
    #signal.alarm(timeout)

    try:
        text = input(prompt)
        signal.alarm(0)
        return text
    #except AlarmException:
    #    return None
    except StopException:
        return ''
    except QuitException:
        return ''
    except KeyboardInterrupt:
        # HACK: Disable for production
        if raw_input_async.last_kill_sig:
            if (time.now() - raw_input_async.last_kill_sig).seconds < config.settings['signals']['sigkill_last']:
                # The user is frantically sending <C-c>s
                if raw_input_async.kill_sigs >= config.settings['signals']['sigkill'] - 1:
                    print('Got <C-c>. ABAAAAAAANDON SHIP!',)
                    exit(0)
            else:
                raw_input_async.kill_sigs = 0
        else:
            raw_input_async.kill_sigs = 0
        raw_input_async.kill_sigs += 1
        raw_input_async.last_kill_sig = time.now()
        # HACK: NOTE: Only this line stays
        return ''
    except EOFError:
        return ''
    finally:
        signal.signal(signal.SIGTSTP, signal.SIG_DFL)
        signal.signal(signal.SIGQUIT, signal.SIG_DFL)
        #signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''

