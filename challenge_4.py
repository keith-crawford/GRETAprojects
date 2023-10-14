#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
# Challenge 4: Make some flask APIs do what you want
# These is a production grade Apache 2.0 webserver running on port 80
# it serves your static folder all the time
# it also serves your apis in src/projectwilliamsville/api.py
# via the api.wsgi file
# you can leave api.wsgi alone, and just add decorated functions to api.py
# your functions in api.py should only pertain to the API wrapper, any actual
# "work" that is done should be done in functions or classes that either
# your scripts or your apis can call.
#
# To start or stop the webserver
# sudo systemctl stop apache2
# sudo systemctl start apache2
#
# or to bounce it
# sudo systemctl restart apache2
#
# You'll see it in VSstudio being tunnelled to your local machine
# http://localhost:80
# to see
#
# You can see auto generated APIDocs here
# http://localhost/apidocs/
# They are based on your good quality docstrings for your api functions
# and clear function labelling.
#
# challenges
# 1. Add a new simple API for a GET end point which returns some json
# - make sure it appears in API docs and you can test it
# 2. Add a new POST end point which accepts in some json processes it and returns it
# 3. Add a GET end point which returns csv text data
# 4. add a GET end point which generates an image and returns an image.
# Extra Credit
# Work out how to make a simple webpage that calls an api...
# ******************************************************************************************************************120

# standard imports

import json

# 3rd party imports
import click
import requests

# custom imports


# declare an exception type so pylint doesn't tell you aren't catching specific enough exceptions.
class MyAPIValidationException(Exception):
    """When response validation fails"""

    def __init__(self, url: str, response, payload: dict = None):
        if payload is None:
            payload = {}
        self.url = url
        self.response = response
        self.payload = payload
        self.message = f'Did not receive 200 from url: {url} {self.response.status_code} {self.response.text}'
        super().__init__(self.message)


# declare a global constant for timeout.
TIMEOUT = 5000



@click.command()


# https://api.parliament.uk/historic-hansard/sittings/2002/apr/16.js

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter