from easypnp_networksys_cz.model import cache
from easypnp_networksys_cz.pnp_dnac import apidnac


class Token(cache.Cache):
    """ Class for managing DNA-C access token """
    def __init__(self):
        """ Creating a constructor """
        # Inheritance which invokes the initialization of the Cache class with a defined parameter ("token")
        super(Token, self).__init__('token')
        # When initializing, save value from cache_config file into self instance __token
        self.__token = self.read_param('token')

    def __str__(self):
        """ Method returns a text representation of self instance __token """
        return str(self.__token)

    def get_new_token(self):
        """ Method to create a new token and save it into cache """
        # Save result of this API call into self instance __token
        self.__token = apidnac.ApiDNAC.api_get_token()
        # Save result to the defined parameter ("token") in file cache_config
        self.save_param('token', self.__token)
        # Return self instance __token
        return self.__token

    def get_token(self):
        """ Method returns the access token saved in self instance __token """
        return self.__token
