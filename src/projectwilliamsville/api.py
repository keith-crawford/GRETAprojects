#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
#
# app.py
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
# 2. Add a new POST end point which accepts in some json processes it and returns it
# 3. Add a GET end point which returns csv text data
# 4. add a GET end point which generates an image and returns an image.
# Extra Credit
# Work out how to make a simple webpage that calls an api...
#
# *********************************************************************************************************************

# standard imports
import json

# 3rd party imports
from flasgger import Swagger
import flask
import pandas

# custom imports
from projectwilliamsville import helpers, keith_mood, providor, hansard

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
def home():
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


@app.route("/earningscall", method=["GET"])
def earncalls() -> dict:
    """ Uses earningcalls function to call them from providor function and post to website
    Except what it actually does is crashes the code with a:
    File "/home/ubuntu/source/project-williamsville/src/projectwilliamsville/api.py", line 85, in <module>
    def earncalls() -> dict:
    TypeError: Rule.__init__() got an unexpected keyword argument 'method'"""

    ereport = providor.earning_calls()
    return ereport

@app.route("/jason", methods=["GET"])
def trypost() -> dict:
    """ Those might actually be the droids we're looking for
    Hope to develop this to posting a jason the stormtrooper as a json to the website
    Works with GET but POST returns : Method Not Allowed
    The method is not allowed for the requested URL."""

    trooper = {
    "Id": "TK-5331",
    "Type": "Stormtrooper",
    "Quantity": 1,
    "Value": 2
    }

    jason = trooper
    #.to_json() - tried to convert trooper to json with this,don't know why it doesn't recognise the method. Pandas and json installed.

    return jason

@app.route("/hansard", methods=["GET"])
def some_other_name_than_hansard():
    """Prints the general hansard json"""
    gibralter=providor.grabawebsite()

    return {
        "Stupid hansard": gibralter
    }

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
      "Providor": providor.NumptyProvidor.gibbergibber(),
      "something_more_impressive": a_numpty.do_something_more_impressive(3)
    }

@app.route("/keith_mood", methods=["GET"])
def get_keith_mood():
    """Start gibbering
    ---
    responses:
        200:
            description: A gibbering function.
    """
    keith = keith_mood.KeithMood(name="Wednesday",level=2)
    mood = keith.improve_mood("chocolate") # +1 = 3
    mood = keith.improve_mood("vape") # doesn't work = 3
    mood = keith.reduce_mood() # -1 = 2 back where started
    return {
      "mood": mood
    }

if __name__ == '__main__':
    app.run()
    # threaded=True by default since Flask 1.0
    # app.run(host="0.0.0.0",port=8000)
