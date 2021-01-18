import requests
import os
import json
from requests_oauthlib import OAuth1Session

# Get secrets
client_key = os.environ['CLIENT_KEY']
client_secret = os.environ['CLIENT_SECRET']
resource_owner_key = os.environ['RESOURCE_OWNER_KEY']
resource_owner_secret = os.environ['RESOURCE_OWNER_SECRET']

# Create OAuth V1.0 session
twitter = OAuth1Session(client_key=client_key,
                        client_secret=client_secret,
                        resource_owner_key=resource_owner_key,
                        resource_owner_secret=resource_owner_secret)

# Send a request to the endpoint using our OAuth V1.0 session
# url = 'https://api.twitter.com/1.1/account/settings.json'
url = "https://api.twitter.com/1.1/statuses/update.json?status=Hello%20again%20World%21"
response = twitter.post(url)

# Print response
print(response.text)