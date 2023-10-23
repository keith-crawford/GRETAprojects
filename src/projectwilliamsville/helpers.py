""" This is some module"""
import math
import random
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

    def this_is_keith(self, person:str) -> str:
        """This turns the variale intokeith"""
        person = "keith"
        return person

def cat() -> str:
    """returns one of three cute cats as a formatted webpage"""
    cat_int = random.randint(1,3)
    # https://www.w3schools.com/html/html_basic.asp
    # https://www.w3schools.com/html/html_images.asp
    web_page = [
        "<!DOCTYPE html>",
        "<html>",
        "<body>",
        "<h1>This is a cat</h1>",
        "<p>A cute cat.</p>",
        f'<img src="../static/img/cats/cat00{cat_int}.jpg" alt="Cute cat #{cat_int}">', # this is why ' are superior,
        "</body>",
        "</html>"
    ]

    return '\n'.join(web_page)
