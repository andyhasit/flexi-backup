import json, os
import sys, inspect
from exceptions import FatalException
from handlers import *


CONFIG_VAR = 'FLEXI_BACKUP_CONFIG'
HANDLERS = dict((format_handler_name(name), cls) for name, cls 
                in inspect.getmembers(sys.modules['handlers'], inspect.isclass)
                if name.endswith('Handler'))


class Config:
    """An object for the overall config"""
    def __init__(self, path=None, targets=None):
        self.path = path
        self.targets = targets


class Target:
    """An individual backup target"""
    def __init__(self, name=None, handler=None):
        self.name = name
        self.handler = handler

    def run(self):
        self.handler.run()


def load_config():
    """
    Returns a Config object loaded from the config file specified by the
    environment variable FLEXI_BACKUP_CONFIG.
    Will raise FatalException if anything is wrong.
    """
    config_file = _get_file_path()
    data = _load_json_from_config_file(config_file)
    targets = _extract_targets(data, config_file)
    return Config(config_file, targets)


def _get_file_path():
    config_file = os.environ.get(CONFIG_VAR)
    if config_file is None:
        raise FatalException('You must set {} in your environment.'.format(CONFIG_VAR))
    if not os.path.isfile(config_file):
        raise FatalException('Environment variable {} must point to a file.'.format(CONFIG_VAR))
    return config_file


def _load_json_from_config_file(config_file):
    with open(config_file, 'r') as fp:
        try:
            data = json.load(fp)
        except json.decoder.JSONDecodeError as e:
            raise FatalException("Error parsing json in config file:\n{}\n{}".format(config_file, e))
    return data


def _extract_targets(data, config_file):
    targets = []
    for name, kwargs in data['targets'].items():
        try:
            if 'cmd' in kwargs:
                assert 'handler' not in kwargs
                handler = 'cmd'
            else:
                assert 'handler' in kwargs
                handler = kwargs['handler']
        except AssertionError:
            raise FatalException(
                'Mistake in config file:\n{}\nEach target must have "cmd" or "handler".'
                .format(config_file))
        targets.append(Target(name, _get_handler(handler, kwargs)))
    return targets


def _get_handler(name, args):
    try:
        handler_cls = HANDLERS[name]
    except KeyError:
        raise FatalException('Handler "{}" not recognised.'.format(name))
    return handler_cls(**args)
