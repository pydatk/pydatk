import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from pydatk import __pydatk_dev
import pydatk

__pydatk_dev.test_pkg('foo')