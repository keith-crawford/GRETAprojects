"""This is a providor of Numpty input"""

# challenges
# 1. Add a new simple API for a GET end point which returns some json
# - make sure it appears in API docs and you can test it
# 2. Add a new POST end point which accepts in some json processes it and returns it
# 3. Add a GET end point which returns csv text data
# 4. add a GET end point which generates an image and returns an image.
# Extra Credit
# Work out how to make a simple webpage that calls an api...

# standard imports - only import what you use.
import random

# 3rd party imports
import requests

# custom imports

# declare global timeout
TIMEOUT = 5000

class NumptyProvidor :
    """Doc string doc string doc string"""

    # if your methods are in classes, they must receive self as a minimum
    def gibbergibber(self) -> str:
        """Make sure you have a docstring"""
        gibberish="Start Gibbering: "
        longeur=random.randint(100,200)
        for i in range(longeur):
            print(i) # do something with the i or don't declare
            num=random.randrange(65,110)
            if num<91:
                let=chr(num)
                gibberish+=let # honestly I would avoid these -= +=  gibberish = gibberish + let better.
            else:
                gibberish+=" "
        # are you trying to return an int or a str?
        return str(gibberish)

def grabawebsite():
    """Just blow the bloody doors off"""

    # This is going to get the full HTML
    # HTML is going to be text, and then you're going to need to Beautiful Soup it (A XML/HTML parser)
    # to work out the bits you want and then be able to do anything with it.

    # also the URL was white - so something is wrong.
    # it should be an object or a string or something - I've made it a strong so it parses.
    # look at what the linter is telling you

    url = "https://api.parliament.uk/historic-hansard/commons/2002/apr/16/gibraltar"

    # Make a response object
    response = requests.request(method="GET",url=url,timeout=10)

    if response.status_code == 200:
        gibralter=response.text
    else:
        gibralter = "It's just a big rock anyway."

    return gibralter

def gibber_gibber_outside_class() -> str:
    """function outside the class, no self"""
    return "gibber gibber"
