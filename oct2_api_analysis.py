#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
# Earnings calls scraper and text analyser
# 1. Downloads data on submitted earnings calls dates and quarters for company and period user requests.
# 2. Finds and compiles appropriate earning calls text.
# 3  Validates the response from the API and provide consistent error handling
# 4. Exports this variable in a .json format usable by other applications
# 5. Performs a textual analysis on the compiled data.
# 6. Creates a wordcloud and saves it as wordcloud.txt in the data folder
# *********************************************************************************************************************

# standard imports
import json

# 3rd party imports
import requests
import click
import pandas
from wordcloud import WordCloud

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

    # Apply a simple textual analysis to demonstrate how the next phase might work.
    print()
    print()


    contents = collatedcalls.lower()
    contents = contents.split(" ")

    # print (contents) # Debugging

    # open stop word list
    stops = open("/home/ubuntu/source/project-williamsville/data/stop_words.txt", "r", encoding="utf-8")
    stoppers = stops.read()
    stop_list = stoppers.split("\n")

    #Remove punctiation and and linebreaks from contents
    punctuation = """!()-—[]{};:"’\,<>./?@#$%^&*_~"""
    linebreak = "\n"


    output_content=list()

    for element in contents:
        if element in punctuation:
            continue
        elif element == linebreak:
            continue
        elif len(element)<4:
            continue
        elif element in stop_list:
            continue
        else:
            output_content.append(element)

    print (f"Length of content: {len(contents)}")
    print (f"Length of output: {len(output_content)}")


    #Create a set from the list. A set cannot have duplicate words, so it returns the individual words.
    content_set=set(output_content)
    print(f"There are {len(content_set)} individual words")
    print("Please wait while most prominent words are calculated...")
    print()

    #Count words and assign quantities to set words, then print in order of quantity
    word_count= {}
    for element in content_set:
        if element not in word_count and element != '':
            total = output_content.count(element)
            word_count[element]=total

    sorted_word_count = sorted(word_count.items(), key= lambda x:x[1], reverse=True)[:10]

    for w in range(len(sorted_word_count)):
        print (w+1, sorted_word_count[w], sep="\t")

    # Make from text - note stopwords are removed automatically
    my_wordcloud = WordCloud().generate(collatedcalls)

    # save to file
    my_wordcloud.to_file("./data/wordcloud.png")
    print()
    print ("Worldcloud saved as png to /home/ubuntu/source/project-williamsville/data/wordcloud.png")

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
