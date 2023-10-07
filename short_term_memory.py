import time
import copy
from dynamo_api import get_short_term_history, put_short_term_history

def filter_and_sort_history(history):
    filtered = []
    current_time = int(time.time())
    for message in history:
        if int(message.get("timestamp")) > current_time - 3600*6: # 6 hours
            filtered.append(message)
    filtered.sort(key=lambda x: x.get("timestamp"))
    return filtered[-50:] # Limited to last 20 messages

def append_history(h, role, message):
    current_time = int(time.time())
    new_history = copy.deepcopy(h)
    new_history.append({"timestamp": current_time, "role": role, "message": message})
    return new_history

def get_short_term_memory(number, user_secret):
    history = get_short_term_history(number, user_secret)
    return filter_and_sort_history(history)

def write_short_term_memory(number, history, user_secret, is_private_on):
    if not is_private_on:
        put_short_term_history(number, filter_and_sort_history(history), user_secret)