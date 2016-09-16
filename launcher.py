"""
A launcher for a pynit service, that can be put in a bashrc.
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
    __import__(serviceFile)
