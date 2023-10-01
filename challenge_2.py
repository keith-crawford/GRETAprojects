#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
#
# challenge_2.py -t <text>
#
# username and password in lastpass
# https://site.financialmodelingprep.com/developer/docs/dashboard/
# API key in last pass
# https://site.financialmodelingprep.com/developer/docs
#
# 0. Work out how to download all the ticker short codes - i.e AAPL (see function)
# 1. Put results into a DataFrame
# 2. Filter the df for just the NASDAQ (which has earning calls)
# 3. Using df.loc operate on a specifc row and column of the data frame of your choice and put that ticker into a var.
# 4. write a new function which accepts a ticker, a quarter and a year, and download the earning call
# 5. please use the provided (modify as you wish) internal _validate function to check the response
# 6. write another function which has sensible arguements and returns and:
#    writes the output to a json file in a sensible directory structure that will allow in the future
#    for many jsons for many tickers for many years and many quarters.
#    make sure the data won't get checked in to github along with your code.
# Extra Credit:
# 7. use df.head to trim the size of your dataframe to 13
# 8. use df.apply to execute your download function for each of 13 rows - no for loops allowed.
#    hint = watch your axis=?
# *********************************************************************************************************************

# standard imports
import json

# 3rd party imports
import requests
import click

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
@click.option('-a', '--apikey', type=str, required=True, help='Don\'t put credentials in your code!')
def main(apikey: str) -> None:
    """Main Function"""
    print(apikey)

    # Which version of APIs to call
    version = "v3"

    # The base url
    baseurl = f"https://financialmodelingprep.com/api/{version}"

    # some APIs will need headers to tell what type of data to return, FMP makes sensible default assumptions.
    headers = {}

    # get some data from the web.
    print(get_stock_market_quote(baseurl, headers, apikey))


def get_stock_market_quote(baseurl: str, headers: dict, apikey: str) -> dict:
    """Does a get of this end point 
    https://site.financialmodelingprep.com/developer/docs/stock-market-quote-free-api/"""

    # work out the URL to call
    api_extension = "/stock/list"
    url = f'{baseurl}{api_extension}?apikey={apikey}'

    # define a payload to send if it's a post
    payload = {}

    response = requests.request("GET", url, headers=headers, data=json.dumps(payload), timeout=TIMEOUT)
    somedumbvariable = _validate_response(response, url)
    return somedumbvariable

def _validate_response(response: requests.Response, url: str, field: str = None, payload: dict = None):
    """Validate the response from the API and provide consistent error handling"""
    if payload is None:
        payload = {}
    if isinstance(response, str) or response.status_code != 200:
        raise MyAPIValidationException(
            url=url, payload=payload, response=response)

    candidate = response.json()
    if candidate:
        if field and field in candidate.keys():
            return candidate[field]
        else:
            return candidate
    else:
        return None


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
