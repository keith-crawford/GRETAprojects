# TODO: fm it's just a bunch of functions.
 
import os

def check_its_a_file(filename:str) -> bool:
    return os.path.isfile(filename)
    
def read_file(filename: str) -> str:
    file_obj = open(filename,mode='r',encoding='utf8')
    file_contents = file_obj.read()
    file_obj.close()
    return file_contents

def write_file(filename: str, contents: str) -> bool:
    file_obj = open(filename,mode='w',encoding='utf8')
    file_obj.write(contents)
    file_obj.close()
    return True

def append_to_file(filename: str, contents: str) -> bool:
    file_obj = open(filename,mode='a',encoding='utf8')
    file_obj.write(contents)
    file_obj.close()
    return True


def print_text(text: str):
    """Please include docstrings"""
    print(text)