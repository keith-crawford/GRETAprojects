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

# This part was dataframes

# The next bit is getting objects from the web and writing it on your server.

# 4. write a new function which accepts a ticker, a quarter and a year, and download the earning call
# 5. please use the provided (modify as you wish) internal _validate function to check the response
# 6. write another function which has sensible arguements and returns and:
#    writes the output to a json file in a sensible directory structure that will allow in the future
#    for many jsons for many tickers for many years and many quarters.
#    make sure the data won't get checked in to github along with your code.


# Extra Credit:
# This function reduces elements in the frame. 
# 7. use df.head to trim the size of your dataframe to 13
# This is probably the most powerful part of pandas: the ability for everyrow of your dataset to be
# able to execute a function on that row.
# 8. use df.apply to execute your download function for each of 13 rows - no for loops allowed.
#    hint = watch your axis=?
# *********************************************************************************************************************

# standard imports
import json

# 3rd party imports
import requests
import click
import pandas
import numpy

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

    #https://financialmodelingprep.com/api/v3/search?query=AA&limit=10&exchange=NASDAQ&(apikey)

    # some APIs will need headers to tell what type of data to return, FMP makes sensible default assumptions.
    headers = {}

    # get some data from the web.
    
    stockdata=get_stock_market_quote(baseurl, headers, apikey=apikey)
    ticker=str
    tickerlimit=int
    exchange=str
    ticker_names=get_ticker_name (baseurl, headers, ticker, tickerlimit, exchange, apikey=apikey)
    enterprise_value=get_company_enterprise_value(baseurl, headers, apikey=apikey)

    #convert list into dataframe
    
    # print(type(stockdata))
    # df = pandas.DataFrame(stockdata)
    # print (df)
    
    # Examples of how to print specific elements from a dataframe
    # print(df.keys())
    # print(df.loc[1, "symbol"])
    # print(df["symbol"])   #Print column
    # print(df.loc[4,])         #Print row
    # print("filter for AAPL:")
    # print(df["symbol"]=="AAPL") #Goes through every row to say true or false
    # print(df[df["symbol"]=="AAPL"]) # Show every row that resolves for filter
    # print(df[df["symbol"]=="AAPL"]) # Does this by putting a truth table into the table

    # dfappl = df[df["symbol"]=="AAPL"]
    # print(dfappl)
    # print(dfappl["symbol"])
    # print(type(dfappl["symbol"]))
    # print(dfappl["price"])
    # print(type(dfappl["price"]))

    #PART 1***************************************************************************************************************
    # 0. Work out how to download all the ticker short codes - i.e AAPL (see function)
    # 1. Put results into a DataFrame
    # 2. Filter the df for just the NASDAQ (which has earning calls)
    # 3. Using df.loc operate on a specifc row and column of the data frame of your choice and put that ticker into a var.

    
    # print("PART 1: Download ticker results into a dataframe then use df.loc to assign specific row and column to a var")
    # df = pandas.DataFrame(ticker_names)
    # chosen_ticker = ("Row 3, Name = ", df.loc[3, "name"])
    # print("Chosen ticker = ",chosen_ticker)

    #PART 2***************************************************************************************************************
    # The next bit is getting objects from the web and writing it on your server.
    # 4. write a new function which accepts a ticker, a quarter and a year, and download the earning call
    # 5. please use the provided (modify as you wish) internal _validate function to check the response
    # 6. write another function which has sensible arguements and returns and:
    #    writes the output to a json file in a sensible directory structure that will allow in the future
    #    for many jsons for many tickers for many years and many quarters.
    #    make sure the data won't get checked in to github along with your code.


    # print()
    # print ("PART 2: Write  afunction to download the arning call, and a second to output to a saved json file")
    # tckr = str(input("Input ticker (eg AAPL, AMD): "))
    # qrtr = int(input("Input quarter (1-4): "))
    # year = int(input("Input year: "))

    # raw_earning_call = get_earning_call(baseurl, headers, apikey, tckr, qrtr, year)
    # df_earn = pandas.DataFrame(raw_earning_call)
    # print(df_earn)
    # earn_sym=df_earn.loc[0, "symbol"]
    # earn_qua=df_earn.loc[0, "quarter"]
    # earn_dat=df_earn.loc[0, "date"]
    
    # output_earning_call(raw_earning_call, earn_sym, earn_qua, earn_dat)

    # Part 3: Extra Credit:
    # This function reduces elements in the frame. 
    # 7. use df.head to trim the size of your dataframe to 13
    # This is probably the most powerful part of pandas: the ability for everyrow of your dataset to be
    # able to execute a function on that row.
    # 8. use df.apply to execute your download function for each of 13 rows - no for loops allowed.
    #    hint = watch your axis=?
# *********************************************************************************************************************
    print()
    print ("PART 3: Use df.head to trim the dataframe to 13 then df.apply to execute download function for each 13 rows")
    
    #Dates of transcripts for particular ticker
    #https://financialmodelingprep.com/api/v4/earning_call_transcript?symbol=AAPL&apikey=3f52741b05f8fdf490e4f7afa3b6083a
    #Returns quarter, year, date
    #This information is sufficient for the output_earning_call function to retun specific reports
    ticker_all = input("Enter the ticker name (eg. AAPL, AMD): ")
    all_transcripts = get_available_transcripts(headers, apikey, ticker_all)
    df_all = pandas.DataFrame(all_transcripts)
    df_all=df_all.head(13)
    print (df_all)


    # x = df.apply(retrieve_earning_call_dates)
    # Two sort of apply
    
    # this is easy to start with 
    # df_all["new_col"] = df_all["just_one_col"].apply() this runs on a column (aka a numpy series)

    # this runs on the full row
    # df_all = df_all.apply(blah,axis=1) this runs on a full row

# A df_apply that actually works!    
#     df_all = df_all[[0,1]].apply(calc_sum)
#     print (df_all)

# def calc_sum(x):
#     print("x=", x)
#     return x.sum()

    # df_all = df_all[[0,1]].apply(retrieve_call_dates, axis=1, args=(baseurl, headers, apikey, ticker_all))
    # print ("New df_all:", df_all)

    earning_calls = df_all[[0,1]].apply(retrieve_call_dates, axis=1, args=(baseurl, headers, apikey, ticker_all))
    print ("Earning calls:", earning_calls) # earning_calls is still a panda dta
    collatedcalls=earning_calls.to_json()
    print(collatedcalls)
    file_obj = open("/home/ubuntu/source/project-williamsville/data/earningreports/collectedreports.txt",mode='w',encoding='utf8')
    file_obj.write(collatedcalls)
    file_obj.close()

def retrieve_call_dates(column: pandas.DataFrame, baseurl, headers, apikey, ticker_all):
    print ("column[0]", column[0])
    print ("column[1]", column[1])

    earning_calls=get_earning_call(baseurl, headers, apikey, ticker_all, column[0], column[1])

    return earning_calls

def get_available_transcripts(headers: dict, apikey: str, ticker_all: str) -> dict:
    """Does a get of this end point
    https://site.financialmodelingprep.com/developer/docs/earning-call-transcript-api/"""


    """https://financialmodelingprep.com/api/v4/earning_call_transcript?symbol=AAPL&apikey=3f52741b05f8fdf490e4f7afa3b6083a"""
    
    #base url not used because this database is v4

    v4url = "https://financialmodelingprep.com/api/v4/earning_call_transcript"
    url = f'{v4url}?symbol={ticker_all}&apikey={apikey}'
    # define a payload to send if it's a post
    payload = {}

    response = requests.request(
        "GET", url, headers=headers, data=json.dumps(payload), timeout=TIMEOUT)
    return _validate_response(response, url)


def output_earning_call(earning_call, symbol, quarter,date):
    
    earning_call=json.dumps(earning_call)  
    file_obj = open(f"/home/ubuntu/source/project-williamsville/data/earningreports/{symbol}Q{quarter}{date}.txt",mode='w',encoding='utf8')
    file_obj.write(earning_call)
    file_obj.close()

    print (f"Report Saved at: /home/ubuntu/source/project-williamsville/data/earningreports/{symbol}Q{quarter}{date}.txt")
  



def get_earning_call(baseurl: str, headers: dict, apikey: str, tckr: str, qrtr:int, year:int) -> dict:
    """Does a get of this end point
    https://site.financialmodelingprep.com/developer/docs/earning-call-transcript-api/"""


    """https://financialmodelingprep.com/api/v3/earning_call_transcript/AAPL?quarter=3&year=2020&apikey=3f52741b05f8fdf490e4f7afa3b6083a"""
    
    # work out the URL to call
    # replace AA&Limit with variable and NASDAQwith a variable
    api_extension = "/earning_call_transcript/"
    url = f'{baseurl}{api_extension}{tckr}?quarter={qrtr}&year={year}&apikey={apikey}'
    # define a payload to send if it's a post
    payload = {}

    response = requests.request(
        "GET", url, headers=headers, data=json.dumps(payload), timeout=TIMEOUT)
    return _validate_response(response, url)




def get_company_enterprise_value(baseurl: str, headers: dict, apikey: str) -> dict:

    """Does a get of this end point
    https://site.financialmodelingprep.com/developer/docs/company-enterprise-value-api/"""
    
    
    #https://financialmodelingprep.com/api/v3/enterprise-values/AAPL?apikey=3f52741b05f8fdf490e4f7afa3b6083a


    # work out the URL to call
    # replace AA&Limit with variable and NASDAQwith a variable
    api_extension = "/enterprise-values/AAPL"
    url = f'{baseurl}{api_extension}?apikey={apikey}'

    # define a payload to send if it's a post
    payload = {}

    response = requests.request(
        "GET", url, headers=headers, data=json.dumps(payload), timeout=TIMEOUT)
    return _validate_response(response, url)


def get_ticker_name(baseurl: str, headers: dict, ticker:str, tickerlimit:int, exchange: str, apikey: str) -> dict:
    """Does a get of this end point https://site.financialmodelingprep.com/developer/docs/stock-ticker-symbol-lookup-api/
    """

    # https://financialmodelingprep.com/api/v3/search?query=AA&limit=10&exchange=NASDAQ&apikey=3f52741b05f8fdf490e4f7afa3b6083a

    # work out the URL to call
    # replace AA & Limit with variable and NASDAQ with a variable
    ticker = "AA"
    limit = 10
    exchange = ""
    api_extension = "/search"
    url = f'{baseurl}{api_extension}?query={ticker}&limit={tickerlimit}&exchange={exchange}&apikey={apikey}'

    # define a payload to send if it's a post
    payload = {}

    response = requests.request(
        "GET", url, headers=headers, data=json.dumps(payload), timeout=TIMEOUT)
    return _validate_response(response, url)


def get_stock_market_quote(baseurl: str, headers: dict, apikey: str) -> dict:
    """Does a get of this end point 
    https://site.financialmodelingprep.com/developer/docs/stock-market-quote-free-api/"""

    # work out the URL to call
    api_extension = "/stock/list"
    url = f'{baseurl}{api_extension}?apikey={apikey}'

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
