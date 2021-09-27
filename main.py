import sys
from config import load_config
from exceptions import FatalException


if __name__ == '__main__':
    try:
        config = load_config()
        if len(sys.argv) > 1:
            specified_targets = sys.argv[1:]
        if specified_targets:
            targets_to_backup = [t for t in config.targets if t.name in specified_targets]
        else:
            targets_to_backup = config.targets
        for target in targets_to_backup:
            print('-' * 80)
            target.run()  # TODO: use threading
    except FatalException as e:
        print(e)
