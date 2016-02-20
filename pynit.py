import multiprocessing, pwd, os, subprocess
#from unittest.mock import patch
from brine import dump,load 

'''
Anything's an init system if you're brave enough!
This is not intended to be used as a system init, but instead as a service manager for microservice based software and web servers like lighttpd.
As of this writing, it's not usable at all. Unless I forgot to remove this line. If it actually has a release and is in pip it's probably fine.
'''

class registry(object):
    '''
    Register a service, so user can start/stop/restart them.
    '''
    services={}
    def __init__(self, socketPath):
        ##Create some kind of rpc here. Probably capnproto, because I want to play with it.
        pass
    def register(func,name):
        def func_wrapper(*args,**kwargs):
            p = func(*args,**kwargs)
            services['name'] = p
            return p
        return func_wrapper

class comment():
#class connection(multiprocessing.connection):
    '''
    Some day this will give us more secure serialization then pickle.
    '''
    def send(self, obj):
        """Send a (brine-able) object"""
        self._check_closed()
        self._check_writable()
        buf = io.BytesIO()
        buf.write(dump(obj))
        self._send_bytes(buf.getbuffer())

    def recv(self):
        """Receive a (brine-able) object"""
        self._check_closed()
        self._check_readable()
        buf = self._recv_bytes()
        return load(buf.getbuffer())

def cd(func,path):
    '''
    Change the working dir of a directory
    '''
    path = os.path.expandvars(path)
    def func_wrapper(*args,**kwargs):
        os.chdir(path)
        p = func(*args,**kwargs)
        return p
    return func_wrapper

def sudo(func,user):
    """
    Run your function as the given user
    Please note that this *permanently* changes user, you won't be able to change back unless you have
    sudo privileges.
    Best used inside @background.
    """
    user = pwd.getpwnam(user)
    def func_wrapper(*args,**kwargs):
        os.setuid(user.uid)
        os.setgid(user.gid)
        p = func(*args,**kwargs)
        return p
    return func_wrapper


def run(func):
   """
   A decorator for running functions. What kind of god could allow a thing such as this?
   """
   def func_wrapper(*args,**kwargs):
       return func(*args,**kwargs)
   func_wrapper()
   return func_wrapper


def background(func):
   """
   Will run you function in the background.
   Please note that there are probably ways to abuse this to run code in the parent.
   In the future, we need to get a serilization method that isn't "pickle" running, for security.

   TODO: Replace the built in pickle? serialization with something else. Maybe rpyc's brine.
   http://stackoverflow.com/a/13019405
   https://docs.python.org/2/library/multiprocessing.html#connection-objects
   """
   def func_wrapper(*args,**kwargs):
       p = multiprocessing.Process(target = func, args=args, kwargs=kwargs)
       p.start()
       return p
   return func_wrapper
