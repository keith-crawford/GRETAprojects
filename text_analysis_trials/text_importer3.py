#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
#
# text_importer.py -f <your_full_path_here>
# Try and use OS to open and write the text file
# Try and use pandas to open and create a dataframe from the CSV
# Try and use json.loads and json.dumps to turn a json to a dict and back again.
# Try and work out the difference between json.loads and json.load
# Extra credit: try and find a big json and use pandas to turn it into a dataframe.
#
# *********************************************************************************************************************

# standard imports
# TODO: look no imports!  in the helper file

# 3rd party imports
import click
import pandas

# custom imports
# TODO: imported it here
import text_analysis_trials.my_helper_file as my_helper_file

# Here is some more helpful examples
@click.command()
@click.option('-f', '--filename', type=str, required=False,default="./data/data.txt",help='Path to file')
@click.option('-c', '--cock', type=str, required=False,default='Giant',help='Honest answers only')
def main(filename: str, cock: str) -> None:
    print(cock)   
    death_list=lazyfunction(plaguedeaths=14, josephgrand="Really lazy")
    death_list=lazyfunction("I am reaaaly lazy", 382)
    print(death_list)
    # f strings are your friend - example of using os
    if my_helper_file.check_its_a_file(filename) == False:
        print(f'Nah fam, not a file: {filename}\n')
    else:
        print(f'YAAAAS it\'s a file: {filename}\n')

    print("Initially")
    # TODO: Check this out
    # just a file full of functions.
    # your executing script can be very simple
    my_helper_file.print_text(my_helper_file.read_file(filename) + "\n")
    
    print("After a complete rewrite - to horse")
    my_helper_file.write_file(filename,contents="horse\n")
    my_helper_file.print_text(my_helper_file.read_file(filename) + "\n")
    
    print("After adding a line - cow ")
    my_helper_file.append_to_file(filename,contents="cow\n")
    my_helper_file.print_text(my_helper_file.read_file(filename) + "\n")
    
    print("After setitng back to original")
    my_helper_file.append_to_file(filename,contents="bush\ntree\nplant\nweed\n")
    my_helper_file.print_text(my_helper_file.read_file(filename) + "\n")
    
    my_helper_file.print_text("Pandas are friendly. We like Pandas.")
    df_neat_table = pandas.read_csv("data/data.csv")
    print(df_neat_table)

    # Example proving it's already a dataframe.
    assert isinstance(df_neat_table,pandas.DataFrame)
    print(type(df_neat_table))

def lazyfunction(josephgrand:str, plaguedeaths:int) -> dict:
    try: 
        assert isinstance(josephgrand, str)
        assert isinstance(plaguedeaths, int)
    except AssertionError:
        print ("String then integer, moron!")
        quit()
    return_dict = {
        "howlazy":josephgrand,
        "plaguedeaths":plaguedeaths
    }
    return return_dict 

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter

