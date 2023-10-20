""" A scrap file to tests modules outside of api.py"""

from projectwilliamsville import providor
import pandas

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

ticker="IBM"
schedule = providor.schedule(ticker)
print('***************Json********************')
print ('schedule:', schedule)
print ('schedule is type ', type(schedule))
print ('**************Dataframe***************')
df = pandas.DataFrame(schedule)
print (df)
df.to_csv("schedule.csv")