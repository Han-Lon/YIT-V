import requests
import os
import json
from requests_oauthlib import OAuth1Session
import urllib
import os
import webbrowser
from kivy.uix.screenmanager import ScreenManager, Screen

# Kivy imports -- do not
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.properties import StringProperty

# Get secrets
client_key = os.environ['CLIENT_KEY']
client_secret = os.environ['CLIENT_SECRET']
# resource_owner_key = os.environ['RESOURCE_OWNER_KEY']
# resource_owner_secret = os.environ['RESOURCE_OWNER_SECRET']


# TODO maybe wrap these authentication methods in a class
# Initial "leg" of the OAuth 3-legged auth method. Get a two keys from Twitter API for delivering users
# to a YIT-V login browser window
def get_resource_token():
    request_session = OAuth1Session(client_key=client_key, client_secret=client_secret)
    url = 'https://api.twitter.com/oauth/request_token'
    response = request_session.get(url)
    response_token = response.text.split('&')
    r_key = response_token[0].split('=')[1]
    r_secret = response_token[1].split('=')[1]
    return [r_key, r_secret]


# Redirect user to Twitter to log in and authorize YIT-V
def get_oauth_verifier(owner_key):
    url = "https://api.twitter.com/oauth/authenticate?oauth_token={}".format(owner_key)
    webbrowser.open(url=url)


# Use the OAuth verifier from above method to get access tokens for this user account
def get_access_token(resource_key, resource_secret):
    verifier = input('\nOAuth Verifier: ')
    twitter = OAuth1Session(client_key=client_key,
                            client_secret=client_secret,
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


def get_twitter_user_session(oauth_token, oauth_secret):
    twitter = OAuth1Session(client_key=client_key,
                            client_secret=client_secret,
                            resource_owner_key=oauth_token,
                            resource_owner_secret=oauth_secret)
    return twitter


# Execute all of the above methods in sequence to authenticate to Twitter
def do_twitter_login():
    keys = get_resource_token()
    get_oauth_verifier(keys[0])
    tokens = get_access_token(keys[0], keys[1])
    return get_twitter_user_session(tokens[0], tokens[1])


class Table(BoxLayout):
    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        self.add_widget(Row("Tweets go here"))

    def update_table(self, tweets):
        try:
            self.remove_widget(Row("Tweets go here"))
        except Exception as e:
            pass
        for tweet in tweets:
            self.add_widget(Row(tweet))


class Row(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(Row, self).__init__(**kwargs)
        self.txt = row


class LoginScreen(Screen):
    def __init__(self, name, sm):
        super().__init__(name=name)
        self.sm = sm

    def do_login(self):
        tw = do_twitter_login()
        self.sm.add_widget(MainWidget(name="MainMenu", session=tw))
        self.sm.current = "MainMenu"


# The main widget for the main menu Kivy app
class MainWidget(Screen):
    def __init__(self, name, session):
        super().__init__(name=name)
        self.session = session

    # Send a request to the endpoint using our OAuth V1.0 session
    def post_tweet(self, content):
        urlsafe = urllib.parse.urlencode({'status': content})
        url = "https://api.twitter.com/1.1/statuses/update.json?{}".format(urlsafe)
        response = self.session.post(url)
        print(response)
        return response

    def get_tweets(self):
        # url = "https://api.twitter.com/2/tweets/1351290770804920321?tweet.fields=created_at,attachments&expansions=author_id"
        # TODO build functionality to save a small amount of recent tweets. Hash the recent tweets file and then compare to see if we need to pull new tweets. This will save on API calls
        url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
        response = self.session.get(url)
        delimiter = '-' * 150
        label_text = []
        for tweet in response.json():
            label_text.append("{delimiter}\nTime: {time} \nUser: {username} \nTweet Body: {body}\n{delimiter}\n\n".format(time=tweet['created_at'],
                                                                                                     username=tweet['user']['screen_name'],
                                                                                                     body=tweet['text'],
                                                                                                     delimiter=delimiter)
                              )
        return label_text

    def on_click(self, tw_btn):
        self.post_tweet(self.tw_tbox.text)
        self.tw_showbox.text = self.tw_tbox.text

    def refresh(self, tw_box):
        self.tw_showbox.clear_widgets()
        for tweet in self.get_tweets():
            self.tw_showbox.add_widget(Row(tweet))


# The main menu for the Kivy app
class MainMenu(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login", sm=sm))
        sm.current = "login"
        return sm


if __name__ == '__main__':
    MainMenu().run()

