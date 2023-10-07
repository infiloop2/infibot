from requests_oauthlib import OAuth1Session
import os
import json

def send_tweet(text, reply_tweet_id):
    # text: str to tweet
    # reply_tweet_id: str or None
    # returns tweet_id or None in case of error
    payload = {
        "text": text
    }
    if reply_tweet_id:
        payload = {
            "text": text,
            "reply": { 
                "in_reply_to_tweet_id": str(reply_tweet_id)
            }
        }

    oauth = OAuth1Session(
        client_key= os.environ.get("twitter_api_key"),
        client_secret= os.environ.get("twitter_api_secret"),
        resource_owner_key= os.environ.get("twitter_owner_access_token"),
        resource_owner_secret= os.environ.get("twitter_owner_access_token_secret"),
    )
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        return None
    
    tweet_id=response.json()['data']['id']
    return tweet_id
