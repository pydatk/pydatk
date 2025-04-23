import logging
import os
import yaml


logger = logging.getLogger(__name__)


logging.warning("""
*******************************************************************************
*   WARNING: __pydatk_dev module contains dev features. Read docs for info.   * 
*******************************************************************************
""")


# YAML

def __yaml_non_dict(deserial, non_dict):
    # parses list of deserialised sections
    # non_dict: 
    #   default 'keep': leave any non-dict values in list
    #   'strip': strip any non-dict values from list
    #   'move': move non-dict items to a list under key 'not_yaml' in the 
    #           preceding dictionary.
    #           items before the first dictionary will be added to a
    #           new dictionary.
    if non_dict == 'keep':
        dicts_only = deserial
    elif non_dict == 'strip':
        dicts_only = [d for d in deserial if type(d) is dict]
    elif non_dict == 'move':
        dicts_only = []
        while len(deserial) > 0:
            item = deserial.pop(0)
            if type(item) is dict:
                dicts_only.append(item)
            elif len(dicts_only) > 0:
                if 'non_dict' in dicts_only[-1].keys():
                    dicts_only[-1]['non_dict'].append(item)
                else:
                    dicts_only[-1]['non_dict'] = [item]
            else:
                dicts_only.append({'non_dict': item})
    else:
        raise Exception('non_dict option not recognised')
    return dicts_only
    
def yaml_deserialize_str(serialized, non_dict='keep'):
    # serialized: string of serialized yaml data (can contain multiple sections)
    # returns list of deserialized sections
    yaml_deserial = yaml.safe_load_all(serialized)
    yaml_deserial = [y for y in yaml_deserial]
    yaml_deserial = __yaml_non_dict(yaml_deserial, non_dict)
    return yaml_deserial

def yaml_deserialize_file(file, non_dict='keep'):
    # file: filename (str) to read serialized data from
    # returns list of deserialized sections
    # non_dict: see __yaml_dict
    if file and os.path.isfile(file):
        with open(file, 'r', encoding='utf-8') as fh:
            yaml_deserial = yaml.safe_load_all(fh)
            yaml_deserial = [y for y in yaml_deserial] # has to be done while yaml generator is open
    else:
        raise Exception('file not found')
    yaml_deserial = __yaml_non_dict(yaml_deserial, non_dict)
    return yaml_deserial

def yaml_serialize(unserialized, file=None, non_dict='keep', start_separator=False, end_separator=False):
    # serialize 'unserialized' data: single section or list (multiple sections)
    # will remove any list items that aren't a dict
    # If 'file' is provided, write serialized data to file then reload to check.
    # non_dict: 
    #   default 'keep': leave any non-dict values in list
    #   'strip': strip any non-dict values from list
    # start/end_separator: If true, adds '---' to start/end of file
    if type(unserialized) is not list: unserialized = [unserialized] 
    if non_dict == 'strip':
        unserialized = [d for d in unserialized if type(d) is dict]       
    elif non_dict != 'keep':
        raise Exception('non_dict option not recognised')
    if file:
        with open(file, 'w', encoding='utf-8') as fh:
            yaml_serial = yaml.safe_dump_all(unserialized, fh, width=79, explicit_start=start_separator, sort_keys=False)
        yaml_deserial = yaml_deserialize_file(file)
    else:
        yaml_serial = yaml.safe_dump_all(unserialized, width=79, explicit_start=start_separator, sort_keys=False)
        yaml_deserial = yaml_deserialize_str(yaml_serial)
    assert unserialized == yaml_deserial, 'check failed'
    if end_separator == True and yaml_serial.strip()[-3:] != '---':
        yaml_serial = yaml_serial.strip() + '\n---\n'
    return yaml_serial
    