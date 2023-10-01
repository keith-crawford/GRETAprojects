#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
#
# json_hints.py -f file TODO: pass your file on the command line
#
# *********************************************************************************************************************

# standard imports
import json
import os

# 3rd party imports
import click

# custom imports



@click.command()
@click.option('-f', '--filename', type=str, required=True, help='Give me a file path!')
def main(filename: str) -> None:
    """Main Function"""
    # check it out
    print_text(filename)
    
    # TODO: try json.load, json.dump
    


def print_text(text: str):
    """Please include docstrings"""
    print(text)

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
