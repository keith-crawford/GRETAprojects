#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
#
# app.py
#
# *********************************************************************************************************************

# standard imports

# 3rd party imports
from flasgger import Swagger
import flask

# custom imports
from projectwilliamsville import helpers

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
        "apidocs": "http://127.0.0.1:80/apidocs"
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
      "something_more_impressive": a_numpty.do_something_more_impressive(3)
    }

if __name__ == '__main__':
    app.run()
    # threaded=True by default since Flask 1.0
    # app.run(host="0.0.0.0",port=8000)
