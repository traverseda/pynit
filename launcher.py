#!/bin/env python3

"""
A launcher for a pynit service, that can be put in a bashrc.

Your first run should be
time python3 -OO launcher.py

add it to your bashrc with
nohup python3 launcher.py &

It will make an ugly line in each new terminal, sorry.
I should make it so it spawns a child, then exits properly.
Then you could run it synchronously, since it's pretty fast.

"""

serviceFile="~/.pynit.py"
pidFile="~/.pynit.lock"

import os
import os.path
serviceFile = os.path.expanduser(serviceFile)
pidFile = os.path.expanduser(pidFile)

if not os.path.isfile(pidFile):
    print("Creating new pynit lock file at ".format(pidFile))
    pid=""
    open(pidFile, "w+").close()
else:
    pid = open(pidFile, "r").read()


def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(int(pid), 0)
    except OSError:
        return False
    else:
        return True

if pid and not check_pid(pid):
    pid=""

if not pid:
    print(serviceFile)
    open(pidFile, "w+").write(str(os.getpid()))
    eval(open(serviceFile,"r+").read())
