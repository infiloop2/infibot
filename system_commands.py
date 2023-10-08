from whatsapp_sender import send_whatsapp_text_reply
from system_messages import get_tweet_system_prompt, found_tweet_context_message,tweet_disallowed_message,get_intro_message, get_quota_left_message, get_deleted_message, get_capabilities_message, get_privacy_message, get_about_message, get_private_mode_off_message, get_private_mode_on_message, get_unsafe_mode_on_message, get_unsafe_mode_off_message, get_all_commands_message
from dynamo_api import get_quota, put_last_privacy_accepted_timestamp, put_private_mode, put_unsafe_mode, put_last_unsafe_accepted_timestamp, put_last_intro_message_timestamp
from short_term_memory import write_short_term_memory, get_short_term_memory
import json
import time
from twitter import send_tweet
import re
from twitter_db_api import append_reply, get_candidate_tweet

# Set this to true when implementation is complete
allow_unsafe_mode = False

def is_system_command(mssg):
    if mssg.lower() == "help":
        return True
    if mssg.lower() == "quota":
        return True
    if mssg.lower() == "examples":
        return True 
    if mssg.lower() == "privacy":
        return True 
    if mssg.lower() == "advanced":
        return True
    if mssg.lower() == "accept privacy":
        return True 
    if mssg.lower() == "history":
        return True 
    if mssg.lower() == "delete":
        return True 
    if mssg.lower() == "private":
        return True 
    if mssg.lower() == "unprivate":
        return True 
    if mssg.lower() == "unsafe":
        return True 
    if mssg.lower() == "safe":
        return True 
    if mssg.lower() == "i take responsibility":
        return True 
    if mssg.lower() == "about":
        return True 
    if mssg.lower() == "reset":
        return True 
    if mssg.lower() == "tweet":
        return True   
    if "pt" in mssg.lower():
        return True
    return False
    
# Returns true if further AI handling is needed, false otherwise
# optionally returns second argument as an additional system message to add before AI
def handle_system_command(mssg, phone_number_id, from_, user_secret, is_private_on, is_unsafe_on):
    if mssg.lower() == "help":
        send_whatsapp_text_reply(phone_number_id, from_, get_intro_message(get_quota(from_)), is_private_on, is_unsafe_on)
        return False, None

    if mssg.lower() == "quota":
        send_whatsapp_text_reply(phone_number_id, from_, get_quota_left_message(get_quota(from_)), is_private_on, is_unsafe_on)
        return False, None

    if mssg.lower() == "examples":
        send_whatsapp_text_reply(phone_number_id, from_, get_capabilities_message(), is_private_on, is_unsafe_on)
        return False, None

    if mssg.lower() == "advanced":
        send_whatsapp_text_reply(phone_number_id, from_, get_all_commands_message(), is_private_on, is_unsafe_on)
        return False, None

    if mssg.lower() == "privacy":
        send_whatsapp_text_reply(phone_number_id, from_, get_privacy_message(), is_private_on, is_unsafe_on)
        return False, None
    
    if mssg.lower() == "accept privacy":
        put_last_privacy_accepted_timestamp(from_, int(time.time()), user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, "Thank you for accepting the privacy policy. You can now chat with me.", is_private_on, is_unsafe_on)
        return False, None

    if mssg.lower() == "history":
        h = get_short_term_memory(from_, user_secret)
        send_whatsapp_text_reply(phone_number_id, from_ , json.dumps(h)[-1500:], is_private_on, is_unsafe_on)
        return False, None

    if mssg.lower() == "delete":
        write_short_term_memory(from_, [], user_secret, is_private_on=False)
        send_whatsapp_text_reply(phone_number_id, from_, get_deleted_message(), is_private_on, is_unsafe_on)
        return False, None

    if mssg.lower() == "private":
        if is_private_on:
            send_whatsapp_text_reply(phone_number_id, from_, "Private Mode is already ON", is_private_on, is_unsafe_on)
            return False, None
        put_private_mode(from_, True, user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, get_private_mode_on_message(), is_private_on, is_unsafe_on)
        return False, None
    
    if mssg.lower() == "unprivate":
        if not is_private_on:
            send_whatsapp_text_reply(phone_number_id, from_, "Private Mode is already OFF", is_private_on, is_unsafe_on)
            return False, None
        if is_unsafe_on:
            send_whatsapp_text_reply(phone_number_id, from_, "Cannot turn off Private mode in Unsafe mode", is_private_on, is_unsafe_on)
            return False, None
        put_private_mode(from_, False, user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, get_private_mode_off_message(), is_private_on, is_unsafe_on)
        return False, None
    
    if mssg.lower() == "unsafe":
        if not allow_unsafe_mode:
            send_whatsapp_text_reply(phone_number_id, from_, "Sorry, Unsafe Mode is under development and not ready yet. Please try again later.", is_private_on, is_unsafe_on)
            return False, None
        if is_unsafe_on:
            send_whatsapp_text_reply(phone_number_id, from_, "Unsafe Mode is already ON", is_private_on, is_unsafe_on)
            return False, None
        put_unsafe_mode(from_, True, user_secret)
        put_private_mode(from_, True, user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, get_unsafe_mode_on_message(), is_private_on, is_unsafe_on)
        return False, None
    
    if mssg.lower() == "safe":
        if not is_unsafe_on:
            send_whatsapp_text_reply(phone_number_id, from_, "Unsafe Mode is already OFF", is_private_on, is_unsafe_on)
            return False, None
        put_unsafe_mode(from_, False, user_secret)
        put_private_mode(from_, False, user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, get_unsafe_mode_off_message(), is_private_on, is_unsafe_on)
        return False, None
    
    if mssg.lower() == "i take responsibility":
        put_last_unsafe_accepted_timestamp(from_, int(time.time()), user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, "Thank you for accepting responsibility. You can now use unsafe mode.", is_private_on, is_unsafe_on)
        return False, None

    if mssg.lower() == "about":
        send_whatsapp_text_reply(phone_number_id, from_, get_about_message(), is_private_on, is_unsafe_on)
        return False, None

    if mssg.lower() == "reset":
        write_short_term_memory(from_, [], user_secret, is_private_on=False)
        send_whatsapp_text_reply(phone_number_id, from_, get_deleted_message(), is_private_on, is_unsafe_on)
        if is_private_on:
            put_private_mode(from_, False, user_secret)
            send_whatsapp_text_reply(phone_number_id, from_, get_private_mode_off_message(), is_private_on, is_unsafe_on)
        if is_unsafe_on:
            put_unsafe_mode(from_, False, user_secret)
            send_whatsapp_text_reply(phone_number_id, from_, get_unsafe_mode_off_message(), is_private_on, is_unsafe_on)
        put_last_intro_message_timestamp(from_,0, user_secret)
        put_last_privacy_accepted_timestamp(from_,0, user_secret)
        put_last_unsafe_accepted_timestamp(from_,0, user_secret)

        return False, None
    
    if mssg.lower() == "tweet":
        if is_unsafe_on or is_private_on:
                send_whatsapp_text_reply(phone_number_id, from_, tweet_disallowed_message(), is_private_on, is_unsafe_on)
                return False, None
        
        history = get_short_term_memory(from_, user_secret)
        if(len(history) < 1):
            send_whatsapp_text_reply(phone_number_id, from_, "No existing history to tweet", is_private_on, is_unsafe_on)
            return False, None
        last_message = history[-1]
        if last_message["role"] != "assistant":
            send_whatsapp_text_reply(phone_number_id, from_, "Last message not by assistant, not tweeting", is_private_on, is_unsafe_on)
            return False, None
        tweet=last_message['message']

        last_found_tweet_id = None
        for msg in reversed(history):
            if msg["role"] == "system" and "tweet_id:" in msg['message']:
                match = re.search("tweet_id:(\d+):", msg['message'])
                if match:
                    last_found_tweet_id = str(match.group(1))
                    send_whatsapp_text_reply(phone_number_id, from_, found_tweet_context_message(last_found_tweet_id, msg['message']), is_private_on, is_unsafe_on)
                    break

        tweet_id=send_tweet(tweet, last_found_tweet_id)
        if tweet_id is None:
            send_whatsapp_text_reply(phone_number_id, from_, "Sorry, tweet failed", is_private_on, is_unsafe_on)
            return False, None
        
        send_whatsapp_text_reply(phone_number_id, from_, "Tweeted [id:"+str(tweet_id)+"]: "+tweet, is_private_on, is_unsafe_on)
        if last_found_tweet_id is not None:
            append_reply(last_found_tweet_id, tweet)
        return False, None
    
    if "pt" in mssg.lower():
        if is_unsafe_on or is_private_on:
            send_whatsapp_text_reply(phone_number_id, from_, tweet_disallowed_message(), is_private_on, is_unsafe_on)
            return False, None
        
        args = mssg.split(" ")
        if len(args) != 3:
            send_whatsapp_text_reply(phone_number_id, from_, "Invalid command. Format should be \"pt username index\"", is_private_on, is_unsafe_on)
            return False, None
        username = args[1]
        index = args[2]

        try:
            const_mapping = {
                0: 'infiloop2',
                1: 'elonmusk',
                2: 'MarioNawfal',
                3: 'POTUS',
                4: 'RishiSunak',
                5: 'PeterSchiff',
                6: 'sama',
                7: 'AISafetyMemes',
                8: 'TiffanyFong_',
                9: 'BillyM2k',
                10: 'ylecun',
                11: 'BanklessHQ',
            }
            username = const_mapping[int(username)]
        except Exception as _:
            None

        tweet = get_candidate_tweet(username, int(index))
        if tweet is None:
            send_whatsapp_text_reply(phone_number_id, from_, "Sorry, tweet not found for user at this index. Try a different user name or a lower index (min 0)", is_private_on, is_unsafe_on)
            return False, None
            
        send_whatsapp_text_reply(phone_number_id, from_, "Pulled tweet[id:"+tweet['tweet_id']+"][username:"+tweet['username']+"]: "+tweet['text'], is_private_on, is_unsafe_on)
        return True, get_tweet_system_prompt(tweet['tweet_id'], tweet['text'])