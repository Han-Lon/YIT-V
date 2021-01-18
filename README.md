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

## Planned features
- A more descriptive README
- A single UI for posting tweets and retrieving your most recent tweets completely
stripped of user interactions
- An "allowlist" of users who you do want to see in your replies
- Ability to send and receive DMs (maybe)
- Implement an NLP-based option so you can analyze the sentiment analysis of your tweets

## Roadmap v0.1
- Implement CLI tool to submit tweets and retrieve most recent tweets (without any 
information regarding retweets, favorites, user interactions, etc)