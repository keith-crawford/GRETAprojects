"""Just a requests example"""

import requests

# get apikey from a protected file
apikey = open('.creds',mode='r',encoding='utf8').read()
print(apikey)

# Hansard example
YYYY=2002
MMM='apr'
D=16
url = f'https://api.parliament.uk/historic-hansard/sittings/{YYYY}/{MMM}/{D}.js'

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
