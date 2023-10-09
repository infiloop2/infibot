import boto3
import os
import time
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource(
    'dynamodb',
    region_name= os.environ.get('aws_region_name'),
    aws_access_key_id=os.environ.get('aws_access_key_id'),
    aws_secret_access_key=os.environ.get('aws_secret_access_key'),
)
tweets_table = dynamodb.Table('infiloop_tweets')

def get_candidate_tweet(username, index):
    response = tweets_table.scan(
        FilterExpression=Attr('username').eq(username)
    )
    items = response['Items']
    sorted_items = sorted(items, key=lambda x: int(x['scrape_timestamp']), reverse=True)
    if index >= len(sorted_items):
        return None
    return sorted_items[index]

def append_reply(tweet_id, reply):
    existing = tweets_table.query(
        KeyConditionExpression=Key('tweet_id').eq(tweet_id)
    )['Items']

    ts = int(time.time())
    if (len(existing) > 0):
        ts = existing[0]['scrape_timestamp']

    tweets_table.update_item(
        Key={
            'tweet_id': tweet_id,
            'scrape_timestamp': ts
        },
        UpdateExpression="set reply=:r",
        ExpressionAttributeValues={
            ':r': str(reply)
        },
    )

