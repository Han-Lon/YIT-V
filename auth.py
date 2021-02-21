from requests_oauthlib import OAuth1Session
import webbrowser


class TwitterLogin():
    """Class for creating an OAuth2 authenticated session to Twitter"""
    def __init__(self, client_key, client_secret):
        self.client_key = client_key
        self.client_secret = client_secret

    # Initial "leg" of the OAuth 3-legged auth method. Get a two keys from Twitter API for delivering users
    # to a YIT-V login browser window
    def get_resource_token(self):
        request_session = OAuth1Session(client_key=self.client_key, client_secret=self.client_secret)
        url = 'https://api.twitter.com/oauth/request_token'
        response = request_session.get(url)
        response_token = response.text.split('&')
        r_key = response_token[0].split('=')[1]
        r_secret = response_token[1].split('=')[1]
        return [r_key, r_secret]


    # Redirect user to Twitter to log in and authorize YIT-V
    def get_oauth_verifier(self, owner_key):
        url = "https://api.twitter.com/oauth/authenticate?oauth_token={}".format(owner_key)
        webbrowser.open(url=url)


    # Use the OAuth verifier from above method to get access tokens for this user account
    def get_access_token(self, resource_key, resource_secret):
        while True:
            verifier = input('\nOAuth Verifier: ')
            if len(verifier) < 1:
                print('No input found. Try again \n')
            else:
                break
        twitter = OAuth1Session(client_key=self.client_key,
                                client_secret=self.client_secret,
                                resource_owner_key=resource_key,
                                resource_owner_secret=resource_secret)
        url = 'https://api.twitter.com/oauth/access_token'
        data = {"oauth_verifier": verifier}
        access_token_response = twitter.post(url, data=data)
        access_tokens_unparsed = access_token_response.text.split('&')
        access_tokens_parsed = []
        for x in access_tokens_unparsed:
            access_tokens_parsed.append(x.split('=')[1])
        return access_tokens_parsed


    def get_twitter_user_session(self, oauth_token, oauth_secret):
        twitter = OAuth1Session(client_key=self.client_key,
                                client_secret=self.client_secret,
                                resource_owner_key=oauth_token,
                                resource_owner_secret=oauth_secret)
        return twitter


    # Execute all of the above methods in sequence to authenticate to Twitter
    def do_twitter_login(self):
        keys = self.get_resource_token()
        self.get_oauth_verifier(keys[0])
        tokens = self.get_access_token(keys[0], keys[1])
        return self.get_twitter_user_session(tokens[0], tokens[1])
