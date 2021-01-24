import requests
import os
import json
from requests_oauthlib import OAuth1Session
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

# Get secrets
# client_key = os.environ['CLIENT_KEY']
# client_secret = os.environ['CLIENT_SECRET']
# resource_owner_key = os.environ['RESOURCE_OWNER_KEY']
# resource_owner_secret = os.environ['RESOURCE_OWNER_SECRET']


# The main widget for the main menu Kivy app
class MainWidget(Widget):
    def on_click(self, tw_btn):
        self.tw_showbox.text = self.tw_tbox.text

    def refresh(self):
        self.tw_showbox.text = "fresh af"


# The main menu for the Kivy app
class MainMenu(App):
    def build(self):
        return MainWidget()


# Creates a new OAuth V1.0 session for accessing Twitter
def get_session():
    # Create OAuth V1.0 session
    twitter = OAuth1Session(client_key=client_key,
                            client_secret=client_secret,
                            resource_owner_key=resource_owner_key,
                            resource_owner_secret=resource_owner_secret)
    return twitter


# tw_session = get_session()
# # Send a request to the endpoint using our OAuth V1.0 session
# # url = 'https://api.twitter.com/1.1/account/settings.json'
# url = "https://api.twitter.com/1.1/statuses/update.json?status=Hello%20again%20World%21"
# response = tw_session.post(url)
#
# # Print response
# print(response.text)

if __name__ == '__main__':
    MainMenu().run()