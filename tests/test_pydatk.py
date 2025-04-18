# OS agnostic - sets path to allow importing pydatk from src
# https://stackoverflow.com/a/34938623/25458574
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

# import pydatk
from pydatk import dev as dtkdev
import pydatk as dtk

# test
print(dtkdev.test_pkg('test pydatk'))

print(dtk.version)
