"""Module for fetching APIs for Hansards"""

# standard imports
import json
import pandas

# 3rd party imports
import requests

# custom imports

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

def get_hansard_commons_report(headers: dict, hansardbaseurl:str,
                               year: int, month: str, date: int, subject: str) -> dict:
    """Does a get of this end point https://api.parliament.uk/historic-hansard/sittings/"""

    # This function used to 'work' in the sense that it didn't crash, but returned a none value.
    # Now it causes a json error that I don't understand.

    #Example https://api.parliament.uk/historic-hansard/commons/2002/apr/16/zimbabwe

    url = f'{hansardbaseurl}/{year}/{month}/{date}/{subject}'
    print (url)


    # define a payload to send if it's a post
    payload = {}

    response = requests.request(
        "GET", url, headers=headers, data=json.dumps(payload), timeout=TIMEOUT)
    return _validate_response(response, url)

def get_hansard_json():
    """Gets hansard json for april 2016"""

    # unbelievably this does get you JSON
    url = "https://api.parliament.uk/historic-hansard/sittings/2002/apr/16.js"
    print (url)


    # define a payload to send if it's a post
    payload = {}

    # ho headers defined before
    headers={}

    response = requests.request(
        "GET", url, headers=headers, data=json.dumps(payload), timeout=TIMEOUT)

    # check if you get a response 200
    if response == 200:
        return response.text
    else:
        return "nah bro"

def fetcher() -> None:
    """what does this do"""

    headers ={}
    hansardbaseurl = "https://api.parliament.uk/historic-hansard/commons/"
    year = 2002
    month = "apr"
    date = 16
    subject = "Zimbabwe"
    print(headers,hansardbaseurl,year,month,date,subject)

    commons_json=get_hansard_json()
    commons_json=pandas.DataFrame(commons_json)
    print(commons_json)

    # commons_report=get_hansard_commons_report(headers, hansardbaseurl, year, month, date, subject)
    # print(commons_report)
    # print(type(commons_report))

def return_blah() -> str:
    """Just returns blah"""
    return "blah"
