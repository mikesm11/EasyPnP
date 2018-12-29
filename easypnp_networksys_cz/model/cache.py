import json


class Cache:
    """ Class responsible for caching config data """
    def __init__(self, name):
        # :param name: name of cached configuration
        self.__file_name = 'cache_config'
        # Cache name of inherited(child) class
        self.__child_name = name
        # Default value is True, children can change
        self.__cacheable = True

    def save_param(self, param_name, param_value):
        c = self.__read_cache()
        if not c.get(self.__child_name):
            c[self.__child_name] = {}
        c[self.__child_name][param_name] = param_value
        self.__save_cache(c)

    def read_param(self, param_name):
        c = self.__read_cache()
        if c.get(self.__child_name) and c[self.__child_name].get(param_name):
            return c[self.__child_name][param_name]
        return None

    def _is_cacheable(self):
        return self.__cacheable

    def _set_cacheable(self, value):
        self.__cacheable = value

    def __read_cache(self):
        """ Content is json string representation """
        content = None
        try:
            file = open(self.__file_name, 'r')
            content = file.read()
            file.close()
        except FileNotFoundError:
            # If file do not exists
            return {}
        try:
            content = json.loads(content)
            return content
        except json.JSONDecodeError:
            # If content is not in json format or is empty
            return {}

    def __save_cache(self, content):
        if not self.__cacheable:
            # If caching of this object is switched off
            return True
        try:
            content = json.dumps(content)
        except:
            # If there is some issue with conversion to json
            return False
        try:
            file = open(self.__file_name, 'w')
            file.write(content)
            file.close()
        except:
            # If there is some issue with writing to file
            return False
        return True
