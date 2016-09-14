from basedir import basedir

import pytest
import os
import shutil
import sys

def main():
    argv = []
    argv.extend(sys.argv[1:])
    pytest.main(argv)

    try:
        os.remove(os.path.join(basedir, '.coverage'))
        shutil.rmtree(os.path.join(basedir, '.cache'))
        shutil.rmtree(os.path.join(basedir, 'tests/.cache'))
    except OSError:
        pass

if __name__ == '__main__':
    main()
