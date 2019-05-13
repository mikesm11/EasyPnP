from easypnp_networksys_cz.model import cache


class Url(cache.Cache):
    """ Class for manipulating with URL address """
    __URL_ADDRESS = 'url'
    __url = ''

    def __init__(self, urlName):
        """ Creating a constructor """
        # Inheritance which invokes the initialization of the Cache class with a defined parameter
        super(Url, self).__init__(urlName)
        # When initializing, save value from cache_config file into self instance __url
        self.__url = self.read_param(self.__URL_ADDRESS)

    def is_set(self):
        """ Method to inform if URL address has been already set """
        # If self instance __url is empty, return False
        if self.__url is None:
            return False
        # Otherwise return True
        return True

    def get_url(self):
        """ Method to get URL address """
        # If URL address has been already set, return current self instance __url
        if self.is_set():
            return self.__url
        # Otherwise return ''
        return ''

    def set_url(self, url):
        """ Method to set URL address """
        # Save entry from parameter (url) into self instance __url
        self.__url = url
        # Save entry from parameter (url) into cache_config file
        self.save_param(self.__URL_ADDRESS, url)

    def __cache_push(self):
        """ Local method for pushing URL address (not yet used) """
        self.save_param(self.__URL_ADDRESS, self.__url)
