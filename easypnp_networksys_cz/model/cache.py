import json


class Cache:
    """ Class responsible for caching config data """
    def __init__(self, name):
        """ Creating a constructor """
        # Name of caching file
        self.__file_name = 'cache_config'
        # Cache name of inherited (child) class
        self.__child_name = name
        # If value is True, entry can be changed
        self.__cacheable = True

    def save_param(self, param_name, param_value):
        """ Public method for saving entries to the cache """
        # Saves the current entries from cache_config file into c object
        c = self.__read_cache()
        # If initialization parameter doesn't exist in cache_config, create entry for that parameter
        if not c.get(self.__child_name):
            c[self.__child_name] = {}
        # Into defined entry (param_name) assign relevant value (param_value)
        c[self.__child_name][param_name] = param_value
        # Saves the new entries from c object into cache_config file
        self.__save_cache(c)

    def read_param(self, param_name):
        """ Public method for reading entries from the cache """
        # Saves the current entries from cache_config file into c object
        c = self.__read_cache()
        # Returns relevant value associated with the selected entry (param_name)
        if c.get(self.__child_name) and c[self.__child_name].get(param_name):
            return c[self.__child_name][param_name]
        # If value doesn't exist, return None
        return None

    def _is_cacheable(self):
        """ Method returns if entry is cacheable """
        return self.__cacheable

    def _set_cacheable(self, value):
        """ Method sets value if entry is cacheable """
        self.__cacheable = value

    def __read_cache(self):
        """ Local method to retrieve data from cache_config file """
        content = None
        # If file exists, save the entries from cache_config file into "content" variable
        try:
            # Open file for reading
            file = open(self.__file_name, 'r')
            content = file.read()
            # Close file
            file.close()
        # If file doesn't exist, return empty dictionary
        except FileNotFoundError:
            return {}
        # Load "content" variable in JSON format and return the result
        try:
            content = json.loads(content)
            return content
        # If "content" variable can't be conversioned or is empty, return empty dictionary
        except json.JSONDecodeError:
            return {}

    def __save_cache(self, content):
        """ Local method to save data into cache_config file """
        # If is caching of this entry switched off, return True
        if not self.__cacheable:
            return True
        # Convert "content" variable to JSON format
        try:
            content = json.dumps(content)
        # If there is some issue with conversion, return False
        except:
            return False
        # If file exists, save the entries from "content" variable into cache_config file
        try:
            # Open file for writing
            file = open(self.__file_name, 'w')
            file.write(content)
            # Close file
            file.close()
        # If there is some issue with writing to the file, return False
        except:
            return False
        # If everything is alright, return True
        return True
