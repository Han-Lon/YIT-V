import requests
import os
import json
from requests_oauthlib import OAuth1Session
import urllib

# Kivy imports -- do not
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

# Get secrets
client_key = os.environ['CLIENT_KEY']
client_secret = os.environ['CLIENT_SECRET']
resource_owner_key = os.environ['RESOURCE_OWNER_KEY']
resource_owner_secret = os.environ['RESOURCE_OWNER_SECRET']


# The main widget for the main menu Kivy app
class MainWidget(Widget):
    def __init__(self, session):
        super().__init__()
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
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?user_id=1350810963298156546"
        response = self.session.get(url)
        delimiter = '-' * 150
        label_text = ""
        for tweet in response.json():
            label_text += "Time: {time} User: {username} Tweet Body: {body}\n{delimiter}\n\n".format(time=tweet['created_at'],
                                                                                                     username=tweet['user']['screen_name'],
                                                                                                     body=tweet['text'],
                                                                                                     delimiter=delimiter)
        return label_text

    def on_click(self, tw_btn):
        self.post_tweet(self.tw_tbox.text)
        self.tw_showbox.text = self.tw_tbox.text

    def refresh(self):
        self.tw_showbox.text = self.get_tweets()


# The main menu for the Kivy app
class MainMenu(App):
    # Creates a new OAuth V1.0 session for accessing Twitter
    def get_session(self):
        # Create OAuth V1.0 session
        twitter = OAuth1Session(client_key=client_key,
                                client_secret=client_secret,
                                resource_owner_key=resource_owner_key,
                                resource_owner_secret=resource_owner_secret)
        return twitter

    def build(self):
        tw_session = self.get_session()
        return MainWidget(tw_session)


if __name__ == '__main__':
    MainMenu().run()