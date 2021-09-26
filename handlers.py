"""
Contains handler classes, whose name must end with "Handler".

In the config file the handler will be named differently:

    RsyncHandler > rsync
    Another_OneHandler > another-one
    Another_One_Handler > another-one
"""
from exceptions import FatalException


def format_handler_name(class_name):
    return class_name.rstrip('Handler').rstrip('_').replace('_', '-').lower()


class BaseHandlerCls:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError()


class RsyncHandler(BaseHandlerCls):
    """
    
    """
    def run(self):
        print('go')

    