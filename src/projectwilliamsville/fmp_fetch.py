""" This is a module to fectch API data from the """

#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-

# standard imports
import json

# 3rd party imports
import requests
import click
import pandas

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

    ## STEP 1: Establish Key variables

    print(apikey)   #Retreived from programme launch

    # Which version of APIs to call
    version = "v3"

    # The base url
    baseurl = f"https://financialmodelingprep.com/api/{version}"

    #https://financialmodelingprep.com/api/v3/search?query=AA&limit=10&exchange=NASDAQ&(apikey)

    # some APIs will need headers to tell what type of data to return, FMP makes sensible default assumptions.
    headers = {}

    ## STEP 2 :Request ticker name and report quantity
    #Then use df.head to trim the dataframe to the requested number of reports.

    print ("Earnings Calls Text Analyser")
    ticker_all = input("Enter the ticker name (eg. XOM, GE, MSFT, BP or C): ")
    quantity = int(input("Enter how many of the most recent earning calls you would like to analyse? "))

    #Call get_available_transcripts to scrape the API list of years and quarters when the company
    all_transcripts = get_available_transcripts(headers, apikey, ticker_all)

    # Convert recovered data into a dataframe of years and quarters
    df_all = pandas.DataFrame(all_transcripts)
    df_all=df_all.head(quantity)

    # Passes the data scraped into the dataframe to retrieve the text of the earnings calls
    # Using df.apply and passing additional arguments established previously (baseurl, headers, apikey, ticker_all)

    earning_calls = df_all[[0,1]].apply(retrieve_call_dates, axis=1, args=(baseurl, headers, apikey, ticker_all))

    # Returned variable earning_calls still a datframe. Convert to json file for compatibility with non-python utilities
    collatedcalls=earning_calls.to_json()

    #Save the json file, which can now be opened by anything from JAVA to EXCELS
    file_obj = open("/home/ubuntu/source/project-williamsville/data/earningreports/collectedreports.txt",mode='w',encoding='utf8')
    file_obj.write(collatedcalls)
    file_obj.close()


#End of main code

def get_available_transcripts(headers: dict, apikey: str, ticker_all: str) -> dict:
    """Does a get of this end point
    https://site.financialmodelingprep.com/developer/docs/earning-call-transcript-api/"""

    #https://financialmodelingprep.com/api/v4/earning_call_transcript?symbol=AAPL&apikey={apikey}

    #Returns quarter, year, date
    #This information is sufficient for the output_earning_call function to retun specific reports

    #base url not used because this database is v4

    v4url = "https://financialmodelingprep.com/api/v4/earning_call_transcript"
    url = f'{v4url}?symbol={ticker_all}&apikey={apikey}'
    # define a payload to send if it's a post
    payload = {}

    response = requests.request(
        "GET", url, headers=headers, data=json.dumps(payload), timeout=TIMEOUT)
    return _validate_response(response, url)

def retrieve_call_dates(column: pandas.DataFrame, baseurl, headers, apikey, ticker_all):
    # prints the current call being processed so user knows that programme is active
    print ("column[0]", column[0])
    print ("column[1]", column[1])

    earning_calls=get_earning_call(baseurl, headers, apikey, ticker_all, column[0], column[1])

    return earning_calls

def get_earning_call(baseurl: str, headers: dict, apikey: str, tckr: str, qrtr:int, year:int) -> dict:
    """Does a get of this end point
    https://site.financialmodelingprep.com/developer/docs/earning-call-transcript-api/"""


    #https://financialmodelingprep.com/api/v3/earning_call_transcript/AAPL?quarter=3&year=2020&apikey={apikey}"""

    # work out the URL to call
    # replace AA&Limit with variable and NASDAQwith a variable
    api_extension = "/earning_call_transcript/"
    url = f'{baseurl}{api_extension}{tckr}?quarter={qrtr}&year={year}&apikey={apikey}'
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
