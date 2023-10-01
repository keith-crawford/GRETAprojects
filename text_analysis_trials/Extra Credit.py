# TODO: python is snake_case extra_credit.py
#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
# TODO: loving it Keith
# Extra credit: try and find a big json and use pandas to turn it into a dataframe.
#
# *********************************************************************************************************************

# standard imports
# TODO: not used
import os

# 3rd party imports
import click
import pandas
# TODO: Standard import
import json

# custom imports

@click.command()
# TODO: text? filename?
@click.option('-t', '--text', type=str, required=False, default='A really big json file', help='Text to print') 
def main(text: str) -> None:

    print(text)

    #Open large file with json
    # TODO: mode! encoding!
    f = open("/home/ubuntu/source/project-williamsville/data/bigfile.json")
    data = json.load(f)
    f.close
    # TODO: nicely closed!
    

    print ("File has been opened and stored in a variable")
    print(data)

    #Tabulate with panda
    neat_table = pandas.DataFrame(data)
    print (neat_table)
    
    # TODO: yep that works!
    # also useful
    neat_table = pandas.json_normalize(data)
    print (neat_table)
    
    # TODO: this will "blow" your mind
    # Then you've got the friends object which is a list within an object
    neat_table = neat_table.explode(["friends"])
    print (neat_table)
    
    # TODO: very nice job.

def print_text(text: str):
    """Please include docstrings"""
    print(text)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
