""" This is some module"""
import math
class Numpty :
    """ This is a numpty """

    def __init__(self) :
        """Instantiate
        """
        self.name = "Numpty"

    def get_name(self) :
        """Connect to the cloudant database configured in config.ini
        """
        return self.name

    def do_something_more_impressive(self, number_a: int) -> str:
        """This does something more impressive with your number"""
        return str(number_a*math.asin(0.4))
