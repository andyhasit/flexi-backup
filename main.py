from config import load_config
from exceptions import FatalException


if __name__ == '__main__':
    try:
        config = load_config()
        for target in config.targets:
            target.run()  # TODO: use threading
    except FatalException as e:
        print(e)
