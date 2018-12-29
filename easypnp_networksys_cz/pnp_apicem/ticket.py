from easypnp_networksys_cz.model import cache
from easypnp_networksys_cz.pnp_apicem import apiapicem


class Ticket(cache.Cache):
    """ Class for managing APIC-EM access ticket """
    def __init__(self):
        super(Ticket, self).__init__('ticket')
        # Read ticket from cache
        self.__ticket = self.read_param('ticket')

    def __str__(self):
        """ Returns a text representation of self instance """
        return str(self.__ticket)

    def get_new_ticket(self):
        """ Creates new ticket and saves it to cache """
        self.__ticket = apiapicem.ApiAPICEM.api_get_ticket()
        self.save_param('ticket', self.__ticket)
        return self.__ticket

    def get_ticket(self):
        """ Returns saved ticket """
        return self.__ticket
