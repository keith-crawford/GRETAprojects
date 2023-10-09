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

headers ={}
baseurl = "https://api.parliament.uk/historic-hansard/sittings/"
year = (int)
month = (str)
date = (int)
@click.command()
@click.option('-y', '--year', type=int, required=True, default='2002', help='Four figure integer, eg. 2002')
@click.option('-m', '--month', type=str, required=True, default="apr", help='jan/feb/mar/apr/may/jun/jul/aug/sep/oct/nov/dec')
@click.option('-d', '--date', type=int, required=True, default=16, help='1-31')

def main(year: int, month: str, date: int) -> None:
    print(get_hansard_report(headers, baseurl, year, month, date))

def get_hansard_report(headers: dict, baseurl:str, year: int, month: str, date: int) -> dict:
    """Does a get of this end point
    https://api.parliament.uk/historic-hansard/sittings/"""

    #Example https://api.parliament.uk/historic-hansard/sittings/2002/apr/16

    url = f'{baseurl}/{year}/{month}/{date}'

    # define a payload to send if it's a post

    payload = {}

    response = requests.request(
        "GET", url, headers=headers, data=json.dumps(payload), timeout=TIMEOUT)
    return _validate_response(response, url)

def _validate_response(response: requests.Response, url: str, field: str = None, payload: dict = None):
    """Validate the response from the API and provide consistent error handling"""
    if payload is None:
        payload = {}
    if isinstance(response, str) or response.status_code != 200:
        raise MyAPIValidationException(
            url=url, payload=payload, response=response)

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter