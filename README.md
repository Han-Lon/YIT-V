# Yodeling into the Void
## A project to make Twitter less toxic
Remove all user interaction metrics from your Twitter usage. 

Don't want to let the fame (or lack thereof) go to your head? Don't want to know if your most recent
🔥🔥🔥 tweet got 1 retweet or 1,000? Just want to **vent** and scream into the void? Try 
yodeling into it instead with Yodeling Into The Void!

## CLI Setup
- ### Windows
  - `pip install -r requirements.txt`
  - `set CLIENT_KEY=<your_api_key>`
  - `set CLIENT_SECRET=<your_api_secret>`
  - `set RESOURCE_OWNER_KEY=<access_token_for_account>`
  - `set RESOURCE_OWNER_SECRET=<access_token_secret_for_account>`
  - `python main.py`
- ### Mac/Linux
  - `pip install -r requirements.txt`
  - `export CLIENT_KEY=<your_api_key>`
  - `export CLIENT_SECRET=<your_api_secret>`
  - `export RESOURCE_OWNER_KEY=<access_token_for_account>`
  - `export RESOURCE_OWNER_SECRET=<access_token_secret_for_account>`
  - `python main.py`
  
## Infrastructure Setup
You'll need a publicly reachable endpoint for Twitter to deliver an "OAuth verifier" in a section of Twitter's
3-legged OAuth credentials process. Refer to the [YIT-V_Infrastructure project](https://github.com/Han-Lon/YIT-V_Infrastructure)
for how to set this up. (It's easy-- most of this process is automated via Docker)

## Planned features
- A more descriptive README
- A single UI for posting tweets and retrieving your most recent tweets completely
stripped of user interactions
- An "allowlist" of users who you do want to see in your replies
- Ability to send and receive DMs (maybe)
- Implement an NLP-based option so you can analyze the sentiment analysis of your tweets
- Ability to upload videos

## Roadmap v0.4
- TBD

## Release Log
- ### v0.3
  - Split Twitter auth into its own class
  - ~~Find some way to securely persist sessions so that each relaunch of the app doesn't require a fresh login~~
    - Per research, there isn't a safe way to do this. Twitter will persist sessions on their end, but fully storing
    the session tokens locally is not a good idea at this time. Not gonna risk a data breach on a hobby side project
  - Image support
  - Add more error handling, especially around posting/retrieving tweets and logging in

- ### v0.2
  - Beautify Kivy GUI
    - Emoji support
    - Nicer background
    - Better contrast between GUI elements
  - Add login screen to dynamically create OAuth sessions instead of relying on environment variables and developer creds
  - ~~Implement a more efficient method of checking recent tweets rather than always calling the API when pressing "Refresh"~~
    - Moving this to a future release. This'll require its own version (non-insignificant work required)
- ### v0.1
  - Functional Kivy-based GUI built out (not pretty yet, but it works 😁)
  - Can post tweets to account using GUI
  - Can retrieve list of user's tweets using GUI. Tweets display in a scrollbox