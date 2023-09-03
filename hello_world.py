#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
#
# hello_world.py -t <text>
#
# *********************************************************************************************************************

# standard imports

# 3rd party imports
import click

# custom imports

@click.command()
@click.option('-t', '--text', type=str, required=False, default='Hello World', help='Text to print')
def main(text: str) -> None:
    """Main Function"""
    print_text(text)

def print_text(text: str):
    """Please include docstrings"""
    print(text)

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
