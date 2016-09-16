import multiprocessing, pwd, os, subprocess, sys, logging
from functools import partial
#from unittest.mock import patch
#from brine import dump,load 

'''
Anything's an init system if you're brave enough!
This is not intended to be used as a system init, but instead as a service manager for microservice based software and web servers like lighttpd.
As of this writing, it's not usable at all. Unless I forgot to remove this line. If it actually has a release and is in pip it's probably fine.

There are two types of things these decorators are designed to run on. Functions (which block) and Service objects (which are thin wrappers around
multiprocessing.Process).
'''

class Service(multiprocessing.Process):
    def __init__(self, *args, name="", **kwargs):
        self.name=name
        super().__init__(*args, **kwargs)

def background(func):
   """
   Will run you function in the background.
   Please note that there are probably ways to abuse this to run code in the parent.
   In the future, we need to get a serilization method that isn't "pickle" running, for security.

   It returns a "Service" object, which right now is pretty much identical to a multiprocess.Process object

   TODO: Replace the built in pickle? serialization with something else. Maybe rpyc's brine.
   http://stackoverflow.com/a/13019405
   https://docs.python.org/2/library/multiprocessing.html#connection-objects
   """
   def func_wrapper(*args,**kwargs):
       p = Service(target = func, args=args, kwargs=kwargs, daemon = False)
       return p
   return func_wrapper

def cd(path):
    '''
    Change the working dir of a program
    '''
    def decorator(func):
        def func_wrapper(*args,**kwargs):
            oldpath = os.getcwd()
            newpath = os.path.expanduser(path)
            os.chdir(newpath)
            p = func(*args,**kwargs)
            os.chdir(oldpath)
            return p
        return func_wrapper
    return decorator

class StreamToLogger(object):
   """
   Fake file-like stream object that redirects writes to a logger instance.
   Used to redirect a programs stdout/stderr to a log file
   """
   def __init__(self, logger, log_level=logging.INFO):
      self.logger = logger
      self.log_level = log_level
      self.linebuf = ''
 
   def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.log_level, line.rstrip())

def log(path, level="INFO", format='%(asctime)s %(levelname)s: %(message)s'):
    '''
    Log the output of a program.
    '''
    newpath = os.path.expanduser(path)
    logging.basicConfig(filename=newpath,level=level, format=format)
    def decorator(func):
        def func_wrapper(*args,**kwargs):
            stdout_logger = logging.getLogger('STDOUT')
            sl = StreamToLogger(stdout_logger, logging.INFO)
            sys.stdout = sl
             
            stderr_logger = logging.getLogger('STDERR')
            sl = StreamToLogger(stderr_logger, logging.ERROR)
            sys.stderr = sl
            p = func(*args,**kwargs)
            return p
        return func_wrapper
    return decorator

def sudo(user):
    raise NotImplemented
    """
    Run your function as the given user
    Please note that this *permanently* changes user, you won't be able to change back unless you have
    sudo privileges.
    Best used inside @background.
    """
    user = pwd.getpwnam(user)
    print(user)
    def decorator(func):
        def func_wrapper(*args,**kwargs):
            os.setuid(user.pw_uid)
            os.setgid(user.pw_gid)
            p = func(*args,**kwargs)
            return p
        return func_wrapper
    return decorator

def run(func):
   """
   A decorator for running functions. What kind of god could allow a thing such as this?
   """
   def func_wrapper(*args,**kwargs):
       return func(*args,**kwargs)
   out = func_wrapper()
   if hasattr(out, 'start'):
       out.start()
   return out
