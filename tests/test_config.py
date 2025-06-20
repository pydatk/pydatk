import configparser
import os
import sys
import tempfile
import unittest
import time

from unittest import mock

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import pydatk as ptk

class TestConfig(unittest.TestCase):

    def tmp_cfg_file(self, test_data):
        # create a config file in tmp dir, with test_data in TestData section
        fn_tmp = tempfile.mkstemp(prefix='config_test_', suffix='.tmp', 
                                    text=True)
        fn_tmp = fn_tmp[1]
        config = configparser.ConfigParser()
        config['TestData'] = test_data
        with open(fn_tmp, 'w') as fh:
            config.write(fh)
        return fn_tmp        

    def test_get_cfg_path_arg(self):
        # test setting and getting a cfg value using arg cfg_path
        cfg_path = self.tmp_cfg_file({'cfg_path_method': 'arg'})
        cfg = ptk.config.Config(cfg_path=cfg_path)
        actual = cfg.get('TestData', 'cfg_path_method')
        expected = 'arg'
        self.assertEqual(actual, expected)

    def test_get_cfg_path_file(self):
        # test setting and getting a cfg value using cfg_path from file
        cfg_path = self.tmp_cfg_file({'cfg_path_method': 'file'})
        config = configparser.ConfigParser()
        config['ConfigPath'] = {
            'config_path': cfg_path
        }
        with open('config_path.ini', 'w') as fh:
            config.write(fh)
        cfg = ptk.config.Config()
        actual = cfg.get('TestData', 'cfg_path_method')
        expected = 'file'
        os.remove('config_path.ini')
        self.assertEqual(actual, expected)

    def test_get_cfg_path_env_var(self):
        # test setting and getting a cfg value using env var cfg_path
        cfg_path = self.tmp_cfg_file({'cfg_path_method': 'env_var'})
        os.environ['CONFIGPATH'] = cfg_path
        self.assertEqual(os.environ.get('CONFIGPATH'), cfg_path)
        cfg = ptk.config.Config()
        actual = cfg.get('TestData', 'cfg_path_method')
        expected = 'env_var'
        self.assertEqual(actual, expected)
        del os.environ['CONFIGPATH']
        self.assertEqual(os.environ.get('CONFIGPATH'), None)

    def test_no_cfg_path(self):
        # tests that exception is raised when no cfg_path is provided
        expected_msg = "Can't determine cfg_path from " \
            "ptk.config.Config(cfg_path), config_path.ini or environment " \
            "variable CONFIGPATH"
        with self.assertRaises(Exception) as cm:  
            cfg = ptk.config.Config()
        self.assertEqual(str(cm.exception), expected_msg)

    def test_set(self):
        # tests setting a config item
        cfg_path = self.tmp_cfg_file({'test': 'set'})
        cfg = ptk.config.Config(cfg_path=cfg_path)
        cfg.set('NewSection', 'new_key', value=99)
        value = cfg.get('NewSection', 'new_key')
        self.assertEqual(value, str(99))

    def test_set_no_cfg_file(self):
        # tests setting a config item when the config file doesn't exist
        fn = os.path.join(tempfile.gettempdir(), 'test_no_file.ini')
        if os.path.exists(fn):
            os.remove(fn)
        self.assertFalse(os.path.exists(fn))
        cfg = ptk.config.Config(cfg_path=fn)
        cfg.set('NewSection', 'new_key', value=99)
        value = cfg.get('NewSection', 'new_key')
        self.assertEqual(value, str(99))
    
    def test_set_no_value(self):
        # tests setting a config item that doesn't have a value
        # (should prompt user to input)
        cfg_path = self.tmp_cfg_file({'test': 'set_no_value'})
        cfg = ptk.config.Config(cfg_path=cfg_path)
        with mock.patch('builtins.input', 
                                 side_effect=['test input']) as mock_input:
            cfg.set('NewSection', 'new_key')
        value = cfg.get('NewSection', 'new_key')
        self.assertEqual(value, 'test input')

    def test_get_section_not_exists(self):
        # tests getting a config item in a section that doesn't exist
        # (should prompt user for value)
        cfg_path = self.tmp_cfg_file({'test': 'set_no_value'})
        cfg = ptk.config.Config(cfg_path=cfg_path)
        with mock.patch('builtins.input', 
                                 side_effect=['input value']) as mock_input:
            cfg.get('NotExist', 'no_key_here')
        value = cfg.get('NotExist', 'no_key_here')
        self.assertEqual(value, 'input value')

    def test_get_section_exists_not_item(self):
        # tests getting a config item in a section that exists but item doesn't
        # (should prompt user for value)
        cfg_path = self.tmp_cfg_file({'test': 'set_no_value'})
        cfg = ptk.config.Config(cfg_path=cfg_path)
        with mock.patch('builtins.input', 
                                 side_effect=['input value']) as mock_input:
            cfg.get('TestData', 'missing_key')
        value = cfg.get('TestData', 'missing_key')
        self.assertEqual(value, 'input value')