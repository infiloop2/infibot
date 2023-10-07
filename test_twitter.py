from twitter import send_tweet
import time

print("Testing send tweet")
tweet_id = send_tweet("Hello World: " + str(time.time()), None)
print("Successfully sent tweet with id", tweet_id)

print("Testing send reply")
tweet_id = send_tweet("Hello again", tweet_id)
print("Successfully sent reply with id", tweet_id)