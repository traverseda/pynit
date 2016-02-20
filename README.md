#Pynit

Pynit is a small library for managing services.

Some day you might be able to use it as an init system.

I'd like to use it with xonsh.

An example of the sort of syntax we want.

```

@run
@background
@sudo("rethink")
def rethinkDBservice():
    rethinkdb &> /var/log/rethink  ##This uses xonsh to run rethinkdb.

```
