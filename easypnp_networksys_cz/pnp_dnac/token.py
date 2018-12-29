from easypnp_networksys_cz.model import cache
from easypnp_networksys_cz.pnp_dnac import apidnac


class Token(cache.Cache):
    """ Class for managing DNA-C access token """
    def __init__(self):
        super(Token, self).__init__('token')
        # Read token from cache
        self.__token = self.read_param('token')

    def __str__(self):
        """ Returns a text representation of self instance """
        return str(self.__token)

    def get_new_token(self):
        """ Creates new token and saves it to cache """
        self.__token = apidnac.ApiDNAC.api_get_token()
        self.save_param('token', self.__token)
        return self.__token

    def get_token(self):
        """ Returns saved token """
        return self.__token
