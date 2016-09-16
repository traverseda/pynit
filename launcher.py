"""
A launcher for a pynit service, that can be put in a bashrc.
"""

serviceFile=".pynit.py"
pidFile=".pynit.lock"

import os.path
if not os.path.isfile(pidFile):
    print("Creating new pynit lock file at ".format(pidFile))
    pid=""
    open(pidFile, "w+").close()

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

if pid and not check_pid(pid):
    pid=""

if not pid:
    import os
    open(pidFile, "w+").write(os.getpid())
    __import__(serviceFile)
