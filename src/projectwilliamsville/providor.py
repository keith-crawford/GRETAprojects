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
import pandas
import json

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

def naminator(name):
    newname=name+"!"+name+"!"+name+"!"
    return newname




###########################
#       FMP SCRAPER       #
###########################

def profiler(ticker: str) -> str:
    """ Retrieves company profile"""
    # get apikey from a protected file
    apikey = open('.creds',mode='r',encoding='utf8').read()

    # do it for whoever - as it's a constant that doesn't get changed here it obeys CAPITALS
    STOCK_TICKER = ticker

    # some FMP apikey you've sorted out - see the parameters
    url = f'https://financialmodelingprep.com/api/v3/profile/{STOCK_TICKER}?apikey={apikey}'

    # Make a response object
    response = requests.request(method="GET",url=url,timeout=10)
    return response.text

def schedule(ticker: str) -> str:
    """ scedule of all earning calls for FMP API using company ticker"""
    # get apikey from a protected file
    apikey = open('.creds',mode='r',encoding='utf8').read()

    # set stock ticker taken from URL
    STOCK_TICKER = ticker

    # This FMP API calls the quarter and year of each earning call
    # eg. [ 2, 2023, "2023-07-19 21:00:20" ]
    url = f'https://financialmodelingprep.com/api/v4/earning_call_transcript?symbol={STOCK_TICKER}&apikey={apikey}'


    #Make a response object
    response = requests.request(method="GET",url=url,timeout=10)

    return response.json()


def schedule_csv(ticker: str) -> str:
    """ schedule of all earning calls for FMP API using company ticker
        at present this saves a CSV to the src folder but returns the response to the GET
        because I don't know how to pass the CSV to the endpoint!
    """
    # get apikey from a protected file
    apikey = open('.creds',mode='r',encoding='utf8').read()

    # set stock ticker taken from URL
    STOCK_TICKER = ticker

    # This FMP API calls the quarter and year of each earning call
    # eg. [ 2, 2023, "2023-07-19 21:00:20" ]
    url = f'https://financialmodelingprep.com/api/v4/earning_call_transcript?symbol={STOCK_TICKER}&apikey={apikey}'


    #Make a response object
    response = requests.request(method="GET",url=url,timeout=10)

    #Make dataframe and saveas csv
    df = pandas.DataFrame(response)
    df.to_csv("src/projectwilliamsville/fmpschedule.csv")

    # The followingcode returns: <_io.TextIOWrapper name='src/projectwilliamsville/fmpschedule.csv' mode='r' encoding='UTF-8'>

    file = open("src/projectwilliamsville/fmpschedule.csv","r")
    csvstring=file
    file.close()

    # So returning csvstring doesn't do what we want - and in fact calls a type error on the website

    return response.text


def get_earning_call(baseurl: str, headers: dict, apikey: str, tckr: str, qrtr:int, year:int) -> dict:
    """Does a get of this end point
    https://site.financialmodelingprep.com/developer/docs/earning-call-transcript-api/"""


    #https://financialmodelingprep.com/api/v3/earning_call_transcript/AAPL?quarter=3&year=2020&apikey={apikey}"""

    api_extension = "/earning_call_transcript/"
    url = f'{baseurl}{api_extension}{tckr}?quarter={qrtr}&year={year}&apikey={apikey}'

    response = requests.request(method="GET",url=url,timeout=10)
    return response.text

def retrieve_call_dates(column: pandas.DataFrame, baseurl:str, headers:dict, apikey:str, ticker_all:str)->dict:
    """ Gets the year and quarter for each earning call on file and returns as dict"""

    earning_calls=get_earning_call(baseurl, headers, apikey, ticker_all, column[0], column[1])

    return earning_calls

def get_available_transcripts(headers:dict, apikey:str, STOCK_TICKER:str)->dict:
    """Does a get of this end point
    https://site.financialmodelingprep.com/developer/docs/earning-call-transcript-api/"""

    #https://financialmodelingprep.com/api/v4/earning_call_transcript?symbol=AAPL&apikey={apikey}

    # This FMP API calls the quarter and year of each earning call
    # eg. [ 2, 2023, "2023-07-19 21:00:20" ]
    url = f'https://financialmodelingprep.com/api/v4/earning_call_transcript?symbol={STOCK_TICKER}&apikey={apikey}'


    #Make a response object
    response = requests.request(method="GET",url=url,timeout=10)

    return response.json()

def earnings_calls(ticker: str) -> str:
    """ Should pull earning calls for FMP API using company ticker
        Starts by getting the schedule
        Then running a df_apply to the earning callsrecord
        """

    # set stock ticker taken from URL
    STOCK_TICKER = ticker

    # get apikey from a protected file
    apikey = open('.creds',mode='r',encoding='utf8').read()

    #set headers
    headers = {}

    #all transcripts is a list of quarter, year, and specific date.
    all_transcripts = get_available_transcripts(headers, apikey, STOCK_TICKER)

    # DEBUGGING - this works to here all_transcripts can be return to endoint

    df_all = pandas.DataFrame(all_transcripts)
    df_all=df_all.head()


    # Convert recovered data into a dataframe of years and quarters
    df_all = pandas.DataFrame(all_transcripts)
    df_all=df_all.head()

    url = "https://financialmodelingprep.com/api/v3"

    earning_calls = df_all[[0,1]].apply(retrieve_call_dates, axis=1, args=(url, headers, apikey, STOCK_TICKER))
    #Returned variable earning_calls still a datframe. Convert to json file for compatibility with non-python utilities
    collated_calls=earning_calls.to_json()

    return collated_calls

###