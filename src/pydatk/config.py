import configparser
import os


class Config:
    """Provides an efficient process for getting and setting 
    configuration items from a .ini configuration file, using Python's
    configparser. 

    It allows a different configuration to be used by the same script
    depending on the environment it's running in (e.g. development vs
    production), without hard-coding configuration file paths.

    It also allows configuration files to be kept outside of a Git
    repository. Consider adding *.ini to .gitignore, especially if using
    the config_path.ini option.

    The location of the configuration file is determined by (in priority
    order): The cfg_path parameter, a config_path.ini file containing a
    path to the configuration file (see below), or a CONFIGPATH 
    environment variable.

    config_path.ini file: This should be in the working directory, with
    a section called ConfigPath and a key called config_path containing
    the path to the required configuration file. 

    The configuration file will be created automatically if it doesn't 
    exist, when the class is instantiated.

    :param cfg_path: The path to the required configuration file.
    :type cfg_path: str, optional
    """

    def __init__(self, cfg_path=None):
        """Constructor method
        """
        # set path to config file: self.cfg_path
        env_var_cfg_path = os.environ.get('CONFIGPATH')
        if cfg_path:
            self.cfg_path = cfg_path
        elif os.path.isfile('config_path.ini'):
            config = configparser.ConfigParser()
            config.read('config_path.ini')
            self.cfg_path = config['ConfigPath']['config_path']
        elif env_var_cfg_path:
            self.cfg_path = env_var_cfg_path
        else:
            raise Exception("Can't determine cfg_path from " \
            "ptk.config.Config(cfg_path), config_path.ini or environment " \
            "variable CONFIGPATH") 
        # call load now to create file if not exists
        self.__load()       

    def __save(self, config):
        """Private method. Saves the configparser object to file.

        :param config: Configparser object to save.
        :type config: configparser.ConfigParser
        """
        with open(self.cfg_path, 'w') as fh:
            config.write(fh)
   
    def __load(self):
        """Private method. Loads a configparser object from file.

        :return: Loaded configparser object.
        :rtype: configparser.ConfigParser
        """
        config = configparser.ConfigParser()
        if not os.path.isfile(self.cfg_path):
            self.__save(config)
            self.__load()
        config.read(self.cfg_path)  
        return config

    def set(self, section, key, value=None):
        """Sets the config section.key to value. The section will be 
        created if it doesn't exist. The config item will be added if it
        doesn't exist. The value is optional: If it isn't provided, the
        user will be asked to input it.

        :param section: Name of .ini file section.
        :type section: str
        :param key: Name of .ini file key.
        :type key: str
        :param value: Value to set.
        :type value: str or None, optional
        """
        config = self.__load()
        if not config.has_section(section):
            config.add_section(section)
        if not config.has_option(section, key):
            if not value:
                value = input(f'Enter config value {section}.{key}: ')
        if not isinstance(value, str):
            value = str(value)
        config.set(section, key, value)
        self.__save(config)

    def get(self, section, key):
        """Gets the config value from the given section.key. If the
        section and key don't exist, they will be created by set() and
        the user will be asked to input the value.

        :param section: Name of .ini file section.
        :type section: str
        :param key: Name of .ini file key.
        :type key: str
        :return: Config value.
        :rtype: str
        """
        config = self.__load()
        if not config.has_section(section):
            self.set(section, key)
            config = self.__load()
        if not config.has_option(section, key):
            self.set(section, key)
            config = self.__load()
        value = config.get(section, key)
        return value
                