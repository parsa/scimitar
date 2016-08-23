# Scimitar
## Ye Distributed Debugger

### Prerequisites
* Software:
  * Python 3 (Python 2 support pending)
  * GDB
* Python Modules
  * pexpect

### Configuration
In order to prevent having to enter the debugging environment configurations every time it is launched and save time Scimitar uses the file `utils/config.py` to retrieve the configurations of a cluster. You may modify and add to it to meet your needs.

### Running
* Launch: Run `scimitar.py` on your machine
* Start a session: `remote <host> <application name> <scheduler job id>`
* Once you're connected you can switch between localities by using the command `switch <locality id>`
