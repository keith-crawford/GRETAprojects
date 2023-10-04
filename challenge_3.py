# here is a very mini example of a class
# try to understand the
# 0.
#   /src/projectwilliamsville module setup
#   read up on python packaging
#   within it create your own file containing your own objects
#   review what this command does: python -m pip install -e .
# 1. function outside of a class
# 1a. import this module and call this function from a script (hint: use the command)
# 1b. make changes on and see around the command when you need to rerun it - or not
# 2. add a class to your module file
# 3. give it some class properties of different types
# 3. validate when you set those they are the right types and throw an Exception if not
# 4. create a class function that operates on those properties
# Extra Credit:
# 5. move a meaningful part of existing work into a file and objects within source
# 5a. have script be core controlling logic only containing functions.


from projectwilliamsville import helpers
a_numpty = helpers.Numpty()
print(a_numpty.do_something_more_impressive(3))