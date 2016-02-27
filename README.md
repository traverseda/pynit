#Pynit

This started as some tools to help me run a bunch of python scripts
that used rethinkdb as a sort of IPC. The idea was to have a "duck typed"
database, where fields get automatically filled in by plugins if they're empty.

You can see the start of that project [here](http://github.com/traverseda/feeds)

Pynit is a small library for managing services.
Some day you might be able to use it as an init system.

It pairs nicely with the [sh library](https://amoffat.github.io/sh/)

*Right now, very little works*

Check the pynit.py file to see what works.
An example of the sort of syntax we want. 

It is only an example, and much of the functionality still doesn't exist.


```
from pynit import *
from sh import rethinkdb

@run
@background
@log("/var/log/rethinkdb.log")
@sudo("rethink")
def rethinkDB_service():
    rethinkdb()

```

A more complicated example


```

from pynit import *
from sh import sshd

#Create a socket to control processes, controlled by root
#Enables commands like "pynit stop $Foo"
root = register("root")

@run
@register
@restart
@root("sshd")
@background
def sshd_service():
    sshd()


```

One of the bigger challenges will be making these somewhat derterministic.

That is, it should't matter too much what order you put the decorators on in.
This is particularily problematic with the "restart" and "register" decorator.

