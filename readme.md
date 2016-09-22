# Scimitar
## Ye Distributed Debugger

### Testing HPX Pretty Printers
* The printers are in the [tools](https://github.com/parsa/scimitar/tree/master/tools) directory.
* To import the printers you have two options:
    * Run `python execfile('PATH_TO_hpx-gdb.py_FILE')`.
    * Run `python sys.path.append('PATH_TO_TOOLS_DIR')`, followed by `import printers`

### Prerequisites
* Software:
  * Python 2.7
  * GDB
* Python Modules
  * pexpect

### Configuration
In order to prevent having to enter the debugging environment configurations
every time it is launched and save time Scimitar uses the file
`utils/config.py` to retrieve the configurations of a cluster. You may modify
and add to it to meet your needs.

### Running
* Schedule a job to run your application. Ensure mpirun starts.
* Run `scimitar.py` on your machine
* Start a session by `remote <host> <scheduler job id>`
* Once you're connected you can switch between localities by using the command `switch <locality id>`

## Commands
* local raw
* local <pid>[ <pid>...]
* local ls
* local ls <regex_pattern>
* remote <machine_name>
* remote <machine_name> <jobid>
* remote <machine_name> attach <app_name> <node:pid>[ <node:pid>...]

### Pending merges:
* GDB/MI
  * MERGE: mi_parser (8ec00bfed88d4beda1c37a516d953638)
* Threads
  * MERGE: thomas_hpx_threads (edccc92d28b14260b1a04930a7e2d836)
* Sessions
  * MERGE: local_session (8c110db273af4a81bea68ef8686f1beb)
  * MERGE: switch_locality (6d52ba7248ed48368d556620d753cbce)
* Report PIDs from HPX
  * MERGE: hpx_pids (4c2e6efda9334f50a97498ff3df4ca37)
* AsyncIO
  * MERGE: asyncio_processing_loop (939bad3d2718407e8b07176c14839ba0)
  * MERGE: live_output (b09de9acc7ad476fb09ce2dd4bd1ad69)
* UI
  * MERGE: ui_wxwidgets (f49ea035cbc845099ac8356d9147dfb0)
  * MERGE: ui_curses (c68045350edc449a90b1dbc4ddbeeb08)
* Pretty Printers
  * MERGE: hpx_printers (adc27b95666b4d2aaa34a4004a055e30)
  * MERGE: natvis_transformer (fecd531769f64374a7848815c9299e57)
  * MERGE: boost_printers (249ae330f2db474fb67a6e79e26853bd)
* config.py
  * MERGE: dotsshconfig (a6206aa120844233b986cb470013cf54)
  * MERGE: stampede_config (3c21aec9daba4bc49fd2d0d98ec0e46b)
  * MERGE: edison_config (613a076ab3254014b55f645a7d85e529)
  * MERGE: cori_config (d8459d9a002047239fb21c3c92050980)
  * MERGE: bigdat_config (406ec14fae894e66ad147245ede1abda)
  * MERGE: supermike2_config (08e71a6fd99246c7ad01e996dd79fea2)
* Interaction with HPX Runtime
  * MERGE: pfx_counters (a4aab1c4f49b48e396b0340924281c22)
  * MERGE: ns_query (1fea6b7c6da446538a35a98f263717fe)
