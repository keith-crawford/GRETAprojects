"""Simplified File Opener"""

import os

# File path to be opened
path = "/home/ubuntu/source/project-williamsville/data/data.txt"
# Flag as R/W
flag = os.O_RDWR 
data_file = os.open(path,flag)
print (data_file, "That's the file")
os.close(data_file)

# TODO: if you use = open method, make sure you data_file.close() when you are done.
# with method closes file for you if I remember.
# I like specific open and closes by the way.
# in general you want to open a file, get the data out, then shutit immediately.
# even if you have to open it again later to add to it.
# it's rare you will be streaming or continously writing to a file unless you are doing some sort of object basd async processing
