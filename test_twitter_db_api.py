from twitter_db_api import get_candidate_tweet, append_reply

print(get_candidate_tweet("MarioNawfal", 0))
print(get_candidate_tweet("MarioNawfal", 1))
print(get_candidate_tweet("unknown", 0))
print(get_candidate_tweet("MarioNawfal", 100000))

append_reply("123", "Hello")
append_reply("123", "Hello")
append_reply("1711133465729540358", "testing...")

print(get_candidate_tweet("MarioNawfal", 0))
print(get_candidate_tweet("MarioNawfal", 1))
print(get_candidate_tweet("MarioNawfal", 2))
print(get_candidate_tweet("MarioNawfal", 3))
print(get_candidate_tweet("MarioNawfal", 4))