import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import pydatk

pydatk.new_module.hello('foo')

print(pydatk.get_version())

