import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import pydatk

yaml_str = """
- Item A
- Item B
- Item C
- Item D
"""

deserial = pydatk.yaml.yaml_deserial_str(yaml_str)

print (deserial)

print(pydatk.yaml.yaml_serial(deserial))