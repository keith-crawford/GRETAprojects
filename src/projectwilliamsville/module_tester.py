""" A scrap file to tests modules outside of api.py"""

from projectwilliamsville import providor

def earncalls() -> dict:
    """Uses earningcalls function to call them from providor function and post to website
        Except what it actually does is crashes the code with a:
        File "/home/ubuntu/source/project-williamsville/src/projectwilliamsville/api.py", line 85, in <module>
        def earncalls() -> dict:
        TypeError: Rule.__init__() got an unexpected keyword argument 'method'"""

    ticker = "IBM"



    ec=providor.earning_calls(ticker)

    return ec

ec=earncalls()

print(ec)
print(type(ec))
