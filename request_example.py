"""Just a requests example"""

import requests

# get apikey from a protected file
apikey = open('.creds',mode='r',encoding='utf8').read()
print(apikey)

# do it for whoever - as it's a constant that doesn't get changed here it obeys CAPITALS
STOCK_TICKER = 'IBM'

# some FMP apikey you've sorted out - see the parameters
url = f'https://financialmodelingprep.com/api/v3/profile/{STOCK_TICKER}?apikey={apikey}'

# Make a response object
response = requests.request(method="GET",url=url,timeout=10)

# Inspect it
print(response)
print(type(response))

# Print the return code
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
print('\nResponse Code: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status')
print(response.status_code)

# Print the text if there is any
print('\nText is a text representation of the JSON here******************')
print(response.text)

# Print the json if there is any
print('\nJSON is the actual thing because FMP plays nice with json*******')
print(response.text)
