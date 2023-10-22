# """ A scrap file to tests modules outside of api.py"""

from projectwilliamsville import providor
import pandas, requests



# def earncalls() -> dict:
#     """Uses earningcalls function to call them from providor function and post to website
#         Except what it actually does is crashes the code with a:
#         File "/home/ubuntu/source/project-williamsville/src/projectwilliamsville/api.py", line 85, in <module>
#         def earncalls() -> dict:
#         TypeError: Rule.__init__() got an unexpected keyword argument 'method'"""

#     ticker = "IBM"



#     ec=providor.earning_calls(ticker)

#     return ec

# ec=earncalls()

# ticker="IBM"
# schedule = providor.schedule(ticker)
# print('***************Json********************')
# print ('schedule:', schedule)
# print ('schedule is type ', type(schedule))
# print ('**************Dataframe***************')
# df = pandas.DataFrame(schedule)
# print (df)

# df.to_csv("src/projectwilliamsville/fmpschedule.csv")

""" schedule of all earning calls for FMP API using company ticker
    at present this saves a CSV to the src folder but returns the response to the GET
    because I don't know how to pass the CSV to the endpoint!
"""
# get apikey from a protected file
apikey = open('.creds',mode='r',encoding='utf8').read()

# set stock ticker taken from URL
STOCK_TICKER = "IBM"

# This FMP API calls the quarter and year of each earning call
# eg. [ 2, 2023, "2023-07-19 21:00:20" ]
url = f'https://financialmodelingprep.com/api/v4/earning_call_transcript?symbol={STOCK_TICKER}&apikey={apikey}'


#Make a response object
response = requests.request(method="GET",url=url,timeout=10)

#Make dataframe and saveas csv
df = pandas.DataFrame(response)
df.to_csv("src/projectwilliamsville/fmpschedule.csv")

file = open("src/projectwilliamsville/fmpschedule.csv","r")
csvstring=file
file.close()

print(csvstring)