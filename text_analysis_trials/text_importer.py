#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
#
# text_importer.py
# Try and use OS to open and write the text file
# Try and use pandas to open and create a dataframe from the CSV
# Try and use json.loads and json.dumps to turn a json to a dict and back again.
# Try and work out the difference between json.loads and json.load
# Extra credit: try and find a big json and use pandas to turn it into a dataframe.
#
# *********************************************************************************************************************

# standard imports
import os

# 3rd party imports
import click
import pandas

# custom imports

@click.command()
@click.option('-t', '--text', type=str, required=False, default='Hello World', help='Text to print') 
def main(text: str) -> None:

    print(text)
    print_data()

    with open("data/data.txt", "w") as data_renew:
        data_renew.write("car\ntree\nbush")
        print("***File Renewed***")
    
    print_data()
   
    with open("data/data.txt", "a") as data_append:
        data_append.write("\nspam")
        print("***Spam Added***")  
    
    print_data()

    #Pandas are friendly. We like Pandas.
    tabulated_data=pandas.read_csv("data/data.csv")
    neat_table = pandas.DataFrame(tabulated_data)
    print (neat_table)

def print_text(text: str):
    """Please include docstrings"""
    print(text)

def print_data():
    with open("data/data.txt", "r") as data_file:
        print(data_file.read())
        print("***")
        print()

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
