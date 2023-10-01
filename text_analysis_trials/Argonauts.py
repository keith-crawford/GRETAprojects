# TODO: argonauts.py Argonauts.py is a class
#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
# Try and use json.loads and json.dumps to turn a json to a dict and back again.
# Try and work out the difference between json.loads and json.load
# Extra credit: try and find a big json and use pandas to turn it into a dataframe.

# *********************************************************************************************************************

# standard imports
import json

# 3rd part imports
import click
import pandas

#custom imports

@click.command()
@click.option('-t', '--text', type=str, required=False, default="Captain of the Argos", 
              help = "May include animated skeletons"
              )
def main(text: str) -> None:
    """Main Function"""
    print_text(text)
    print("********************")
    print()


#read csv file and create dictionary
    csvfilepath='/home/ubuntu/source/project-williamsville/data/argodata.csv'


    ## Crude version
    #  with open(csvfilepath, 'r', encoding='utf8') as file:
    #     reader = csv.reader(file)
    #     headers = next(reader)  #read the header row

    #     argosdata = []
    #     for row in reader:
    #         record = {}
    #         for i, value in enumerate(row):
    #             record[headers[i]] = value
    #         argosdata.append(record)
    # print(f"argosdata: {argosdata}")

    # Dictionary creates from csv with Pandas
    data = pandas.read_csv(csvfilepath)
    argosdata = data.to_dict()

    print (f"Argos Crew: {argosdata}")

    # # #Add Argus to the crew - Argus, 3, Argos, Arestor
    # This doesn't work - it adds Argus into the first level of the dictionary and I don't know how to change that.
    # argosdata["name"] = "Argus"
    # argosdata["sources"] = 3
    # argosdata["abode"] = "Argos"
    # argosdata["parent"] = "Arestor"

    # print(f"argosdata with argus: {argosdata}")

    # Serializing json
    # TODO: loving the indent
    json_object = json.dumps(argosdata, indent = 4)
    print(f"Json conversion of Python dict: {json_object}")

    # create new json file and write argosdata in it
    # TODO: encoding='utf8' one day this habbit will save you nights of sleep.
    with open("argos_away.json", "w") as write_file:
        json.dump(argosdata, write_file)

    # open argos_away.json as a data type 
    with open("argos_away.json", "r") as read_file:
        crew_list = json.load(read_file)
    
    print (f"Final crew list {crew_list}")
    print("********")
    print(type(crew_list))
    print()

    print("What does json.loads do?")
    print("json.load() reads a JSON document from file")
    print("json.loads() is used to convert a json string into a python dictionary")
    
    crew_string=json.dumps(crew_list)
    captain_list=json.loads(crew_string)
    print(captain_list)


def print_text(text:str):
    """Please include docstrings"""
    print(text)

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter

