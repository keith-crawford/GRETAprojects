#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
#
# text_analyser.py -f <your_input_file_here
#
# TODO: you were getting \\n stuff in your text becuase the file was a json file and it delimits the text
# json module sorts that for you.
# if you title the file <whatever>.json vscode has helpers for you.
#
# *********************************************************************************************************************

# standard imports
import json

# custom imports
import nltk
import click
import pandas


# Here is some more helpful examples
@click.command()
@click.option('-f', '--filename', type=str, required=False,default="./data/example_report.json",help='Path to json file')
@click.option('-d', '--nltkdatapath',type=str, default = '/home/ubuntu/source/project-williamsville/data/nltk_data', help='Where to put the stopwords etc')
def main(filename: str, nltkdatapath: str) -> None:
    
    # make sure your file is saved as a json
    if not filename.endswith('.json'):
        print(f'Please pass a json file name: {filename}')
        
    # open and read the json to a dict - dict is the equivilant object internally in python
    # json is only when written to the file.  
    with open(filename, mode='r',encoding='utf8') as json_file:
        dict_from_json = json.load(json_file)
        # this json is actually a list of results, so we are going to the first one of them
        dict_from_json = dict_from_json[0]
        # sometimes if a function doesn't declare it's return, or could have multiple types of returns.
        # or if it might return null - vscode won't know what type it is.
        # if you know, then assert it and vscode will read this and understand
        # then methods like .keys() will autoprompt
        assert isinstance(dict_from_json,dict)
        
    print(f'These are the keys from the json file {dict_from_json.keys()}')
    
    # we want the content as a big string
    content = dict_from_json["content"]
    assert isinstance(content, str)
    
    # we can lowercase it, but arguable whether we want to do this generally - but for the counts it's probably useful
    content = content.lower()
       
    # then we tokenize using the whitespace (basic) nltk tokenizer - instead of doing split
    contents = nltk.tokenize.WhitespaceTokenizer().tokenize(content)
    
    # get a stopworld list from nltk instead of a file
    # note we are again really tightly controlling where nltk sticks stuff so we can see it
    # it will only redownload it if not there
    # try deleting stopwords in ./data/nltk_data/
    try:
        nltk.data.find('corpora/stopwords',paths=[nltkdatapath])
    except LookupError:
        nltk.download('stopwords',download_dir=nltkdatapath)
    
    # stop words is in white because downloading modules in code is bad - on my list of things to fix one day.
    stop_list = nltk.corpus.stopwords.words('english')
    
    # pandas are beautiful creatures
    df = pandas.DataFrame(contents,columns=['token'])
                          
    # eliminate your stop words ~ means reverse the truth table
    print(f'before df has shape: {df.shape}')
    df = df[~df["token"].isin(stop_list)]
    print(f'after df has shape: {df.shape}')
    
    # doing some lemmatization as well
    try:
        nltk.data.find('corpora/wordnet',paths=[nltkdatapath])
    except LookupError:
        nltk.download('wordnet',nltkdatapath)
    lemmatizer = nltk.stem.WordNetLemmatizer()
    df["lemma"] = df["token"].apply(lemmatizer.lemmatize)
     
    # do a count up here we are counting the token column, based on gropuing by the lema
    df = df.groupby(["lemma"]).count()
    
    # do a sort
    df = df.sort_values('token',ascending=False)
    
    # reset the index to be the position because that's nice
    df = df.reset_index(drop=False)
    
    # print the top n - see ibm at 16
    print(df.head(50))

    # so of the four checks previously
    # for element in contents:
    #     if element in punctuation:               The punctuation char replace doesn't work like you want it, generally we want to tackle punctuation at the tokeniszer leevel - the spacy tokenizer is nice.
    #         continue
    #     elif element == linebreak:               Linebreaks are coming out with the whitespace tokenizer tab, newline and space
    #         continue
    #     elif len(element)<4:                     I know this is common but do we want it?  IBM is the ticket, and they mention that 16th most common.
    #         continue
    #     elif element in stop_list:               THe pandas bit does this lookup for you for each row.
    #         continue
    #     else: 
    #         output_content.append(element)        


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter