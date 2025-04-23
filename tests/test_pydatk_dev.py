import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from pydatk import __pydatk_dev
import pydatk

# YAML

yaml_str = """
- Item A
- Item B
- Item C
- Item D
"""

deserial = __pydatk_dev.yaml_deserialize_str(yaml_str)
print(deserial)

print(__pydatk_dev.yaml_serialize(deserial))