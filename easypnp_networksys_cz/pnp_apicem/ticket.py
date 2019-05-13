from easypnp_networksys_cz.model import cache
from easypnp_networksys_cz.pnp_apicem import apiapicem


class Ticket(cache.Cache):
    """ Class for managing APIC-EM access ticket """
    def __init__(self):
        """ Creating a constructor """
        # Inheritance which invokes the initialization of the Cache class with a defined parameter ("ticket")
        super(Ticket, self).__init__('ticket')
        # When initializing, save value from cache_config file into self instance __ticket
        self.__ticket = self.read_param('ticket')

    def __str__(self):
        """ Method returns a text representation of self instance __ticket """
        return str(self.__ticket)

    def get_new_ticket(self):
        """ Method to create a new ticket and save it into cache """
        # Save result of this API call into self instance __ticket
        self.__ticket = apiapicem.ApiAPICEM.api_get_ticket()
        # Save result to the defined parameter ("ticket") in file cache_config
        self.save_param('ticket', self.__ticket)
        # Return self instance __ticket
        return self.__ticket

    def get_ticket(self):
        """ Method returns the access ticket saved in self instance __ticket """
        return self.__ticket
