import requests
import os
import json
from auth import TwitterLogin
import urllib
import os
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime

# Kivy imports -- do not remove these even if your IDE says they are not in use!
from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.properties import StringProperty

# tkinter import for file dialogue box. MUCH easier than kivy's file dialogue
import tkinter
from tkinter.filedialog import askopenfilename

# Get secrets
client_key = os.environ['CLIENT_KEY']
client_secret = os.environ['CLIENT_SECRET']
# resource_owner_key = os.environ['RESOURCE_OWNER_KEY']
# resource_owner_secret = os.environ['RESOURCE_OWNER_SECRET']

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
        tw_class = TwitterLogin(client_key=client_key, client_secret=client_secret)
        tw = tw_class.do_twitter_login()
        self.sm.add_widget(MainWidget(name="MainMenu", session=tw))
        self.sm.current = "MainMenu"


# The main widget for the main menu Kivy app
class MainWidget(Screen):
    def __init__(self, name, session):
        super().__init__(name=name)
        self.session = session

    # Send a request to the endpoint using our OAuth V1.0 session
    def post_tweet(self, content, media_ids=None):
        url_dict = {}
        url_dict['status'] = content
        if media_ids is not None:
            url_dict['media_ids'] = media_ids
        if self.tw_sensitive.active:
            url_dict['possibly_sensitive'] = "true"
        urlsafe = urllib.parse.urlencode(url_dict)
        url = "https://api.twitter.com/1.1/statuses/update.json?{}".format(urlsafe)
        response = self.session.post(url)
        if response.status_code != 200:
            raise ValueError("Error! Expecting response status 200, received {}\n Response JSON: {}".format(response.status_code, response.json()))
        print(response)
        return response

    def get_tweets(self):
        # url = "https://api.twitter.com/2/tweets/1351290770804920321?tweet.fields=created_at,attachments&expansions=author_id"
        # TODO build functionality to save a small amount of recent tweets. Hash the recent tweets file and then compare to see if we need to pull new tweets. This will save on API calls
        url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
        response = self.session.get(url)
        if response.status_code != 200:
            raise ValueError("Error! Expecting response status 200, received {}\n Response JSON: {}".format(response.status_code, response.json()))
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

    def upload_media(self):
        filename = askopenfilename(filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.gif"),
                                              ("All file", "*.*"))
                                   )
        if filename is None or filename is '':
            print("No valid file selected. Returning...\n")
            return None
        with open(filename, 'rb') as media_file:
            media_data = media_file.read()
        urlsafe = urllib.parse.urlencode({'media_category': "tweet_image"})
        url = "https://upload.twitter.com/1.1/media/upload.json?{}".format(urlsafe)
        print("Uploading image... \n")
        response = self.session.post(url, files={"media": media_data})

        if response.status_code != 200:
            raise ValueError("Error! Expecting response status 200, received {}\n Response JSON: {}".format(response.status_code, response.json()))
        print("Upload image result: {}\n".format(response.status_code))
        print('Retrieved media ID, sending status update...\n')
        if self.tw_tbox.text is None or self.tw_tbox.text == "":
            self.post_tweet(content="Test", media_ids=response.json()['media_id'])
        else:
            self.post_tweet(content=self.tw_tbox.text, media_ids=response.json()['media_id'])

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
    # tkinter related code for the media upload file dialogue-- if this isn't here, an empty Tkinter frame pops up when uploading media
    tk_root = tkinter.Tk()
    tk_root.withdraw()

    # Weird Kivy bug where right clicking with a mouse with multi-touch emulation mode enabled
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

    MainMenu().run()

