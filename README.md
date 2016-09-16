#Pynit

This started as some tools to help me run a bunch of python scripts
that used rethinkdb as a sort of IPC. The idea was to have a "duck typed"
database, where fields get automatically filled in by plugins if they're empty.

Pynit is a small library for managing services.
Some day you might be able to use it as an init system.

Right now, the big disadvantage is that you can't dynamically reload services,
and it doesn't automatically restart on changes.

It pairs nicely with the [sh library](https://amoffat.github.io/sh/)
and the [schedule](https://github.com/dbader/schedule) library for cron-like
behavior.

```
from pynit import *
import sh

@run
@background
@cd(~/)
@log("~/.logs/rethinkdb.log")
def runRethinkDB():
    sh.rethinkdb(_iter=True)
 
```
