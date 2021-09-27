"""
Contains handler classes, whose name must end with "Handler".

In the config file the handler will be named differently:

    RsyncHandler > rsync
    Another_OneHandler > another-one
    Another_One_Handler > another-one
"""
import sys, subprocess
from exceptions import FatalException


def format_handler_name(class_name):
    return class_name[:-len('Handler')].rstrip('_').replace('_', '-').lower()


class BaseHandlerCls:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError()


class RsyncHandler(BaseHandlerCls):
    """
    
    """
    def run(self):
        print(self.kwargs)


class CmdHandler(BaseHandlerCls):
    """
    Runs the specified command.
    """
    def run(self):
        cmd = self.kwargs.get('cmd')
        print(cmd)
        process = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE)
        # TODO determine if error and print red
        output, errors = process.communicate()
        for line in output.splitlines():
            print(line)
        
    