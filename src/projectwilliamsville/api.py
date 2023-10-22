#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
# app.py
#
# NOTES: Functions not working as intended are as follows:
# def earning calls - fails TypeError: Rule.__init__() got an unexpected keyword argument 'method'
# def trypost - works fine as a get, put it was suppost to be a POST
# def collatedcalls - meant to send json to api docs but doesn't work
#
#
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
# 2. Accept parameters for things you want to and return json incorporating them.
# 3. Add a GET end point which returns csv text data
# 4. add a GET end point which generates an image and returns an image.
# Extra Credit
# Work out how to make a simple webpage that calls an api...
#
# *********************************************************************************************************************

# standard imports

# 3rd party imports
from flasgger import Swagger
import flask
import requests

# custom imports
from projectwilliamsville import helpers, keith_mood, hansard, providor

app = flask.Flask(__name__)
template = {
  "swagger": "2.0",
  "info": {
    "title": "Project-Williamsville",
    "description": "APIs for content analytics",
    "version": "0.0.1"
  }
}
swagger = Swagger(app, template=template)

app.config["DEBUG"] = True

@app.route("/", methods=["GET"])
def home() -> dict:
    """Welcome message
    ---
    responses:
        200:
            description: A welcome message
    """

    return {
        "text": "Welcome to Project-Williamsville",
        "apidocs": "http://127.0.0.1:80/apidocs",
        "blah": hansard.return_blah()
    }

@app.route('/profile/<ticker>')
def profile(ticker:str) -> str:
     """"calls FMP API for company profile for ticker in URL
    ---
    responses:
        200:
            description: FMP Company Profiles
    """
     stockticker=ticker
     return providor.profiler(stockticker)

@app.route('/earningscalls/<ticker>')
def earncalls(ticker:str) -> str:
    """"calls FMP API for company earnings calls for ticker in URL
    ---
    responses:
        200:
            description: FMP Company Earning Calls
    """
    stockticker=ticker
    return providor.earnings_calls(stockticker)

@app.route('/schedules/<ticker>')
def schedule(ticker:str) -> str:
    """"calls FMP API for quarters, years, and times of all recorded earning calls.
    ---
    responses:
        200:
            description: FMP Company Earning Calls
    """

    stockticker=ticker
    return providor.schedule(stockticker)

############## WORK IN PROGRESS - RETURNING A CSV##############

@app.route('/schedulecsv/<ticker>')
def schedulecsv(ticker:str) -> str:
    """"calls FMP API for quarters, years, and times of all recorded earning calls and returns a CSV file
    ---
    responses:
        200:
            description: FMP Company Earning Calls
    """

    stockticker=ticker
    return providor.schedule_csv(stockticker)




###########################
#      FILE UPLOAD        #
###########################

@ app.route('/picture')
def picture_loader():
    """Posts KeithandStephen.jpg from src folder to endpoint
    ---
    responses:
        200:
            description:
    """
    url = 'http://127.0.0.1:5000/picture'
    pic = {'media': open('/home/ubuntu/source/project-williamsville/src/projectwilliamsville/KeithandStephen.jpg', 'rb')}

    response = requests.post(url=url, files=pic)
    return  response.text


# ******************************************************************************************************************120
# Test functions
# *********************************************************************************************************************

@ app.route('/nametastic/<name>')
def name800(name: str) ->str:
    """It absolutely will not stop until it finds the method error"""
    oyname=providor.naminator(name)
    return f'Oy! {oyname}'

@app.route('/hello/<name>')
def hello_name(name:str) -> str:
    """returns Hello + folder name to hello/<name>endpoint
    ---
    responses:
        200:
            description:
    """
    return f'Hello {name}!'

@app.route("/jason", methods=["GET"])
def jason() -> dict:
    """A stormtrooper called Jason.
    ---
    responses:
        200:
            description: A stormtrooper called Jason.
    """

    trooper = {
    "Id": "TK-5331",
    "Type": "Stormtrooper",
    "Quantity": 1,
    "Value": 2,
    "Accuracy": 0
    }

    return trooper

@app.route("/gibber", methods=["GET"])
def gibber():
    """Start gibbering
    ---
    responses:
        200:
            description: A gibbering function.
    """
    a_numpty = helpers.Numpty()
    return {
      "objectname": a_numpty.get_name(),
      "Providor": "tree",
      "something_more_impressive": a_numpty.do_something_more_impressive(3)
    }

@app.route("/keith_mood/<ingest>", methods=["GET"])
def get_keith_mood(ingest:str) -> dict:
    """Start gibbering
    ---
    responses:
        200:
            description: A gibbering function.
    """
    keith = keith_mood.KeithMood(name="Wednesday",level=2)
    mood = keith.improve_mood(ingest)

    return {
      "mood": mood
    }

if __name__ == '__main__':
    app.run()
    # threaded=True by default since Flask 1.0
    # app.run(host="0.0.0.0",port=8000)
