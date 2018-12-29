from easypnp_networksys_cz.model import cache


class Url(cache.Cache):
    """ Class for manipulating with URL object """
    __URL_ADDRESS = 'url'
    __url = ''

    def __init__(self, urlName):
        super(Url, self).__init__(urlName)
        self.__url = self.read_param(self.__URL_ADDRESS)

    def is_set(self):
        if self.__url is None:
            return False
        return True

    def get_url(self):
        if self.is_set():
            return self.__url
        return ''

    def set_url(self, url):
        self.__url = url
        self.save_param(self.__URL_ADDRESS, url)

    def __cache_push(self):
        self.save_param(self.__URL_ADDRESS, self.__url)
