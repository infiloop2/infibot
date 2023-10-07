from whatsapp_sender import send_whatsapp_text_reply
from system_messages import found_tweet_context_message,tweet_disallowed_message,get_intro_message, get_quota_left_message, get_deleted_message, get_capabilities_message, get_privacy_message, get_about_message, get_private_mode_off_message, get_private_mode_on_message, get_unsafe_mode_on_message, get_unsafe_mode_off_message, get_all_commands_message
from dynamo_api import get_quota, put_last_privacy_accepted_timestamp, put_private_mode, put_unsafe_mode, put_last_unsafe_accepted_timestamp, put_last_intro_message_timestamp
from short_term_memory import write_short_term_memory, get_short_term_memory
import json
import time
from twitter import send_tweet
import re

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
    return False
    
def handle_system_command(mssg, phone_number_id, from_, user_secret, is_private_on, is_unsafe_on):
    if mssg.lower() == "help":
        send_whatsapp_text_reply(phone_number_id, from_, get_intro_message(get_quota(from_)), is_private_on, is_unsafe_on)
        return

    if mssg.lower() == "quota":
        send_whatsapp_text_reply(phone_number_id, from_, get_quota_left_message(get_quota(from_)), is_private_on, is_unsafe_on)
        return

    if mssg.lower() == "examples":
        send_whatsapp_text_reply(phone_number_id, from_, get_capabilities_message(), is_private_on, is_unsafe_on)
        return

    if mssg.lower() == "advanced":
        send_whatsapp_text_reply(phone_number_id, from_, get_all_commands_message(), is_private_on, is_unsafe_on)
        return

    if mssg.lower() == "privacy":
        send_whatsapp_text_reply(phone_number_id, from_, get_privacy_message(), is_private_on, is_unsafe_on)
        return
    
    if mssg.lower() == "accept privacy":
        put_last_privacy_accepted_timestamp(from_, int(time.time()), user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, "Thank you for accepting the privacy policy. You can now chat with me.", is_private_on, is_unsafe_on)
        return

    if mssg.lower() == "history":
        h = get_short_term_memory(from_, user_secret)
        send_whatsapp_text_reply(phone_number_id, from_ , json.dumps(h)[-2000:], is_private_on, is_unsafe_on)
        return

    if mssg.lower() == "delete":
        write_short_term_memory(from_, [], user_secret, is_private_on=False)
        send_whatsapp_text_reply(phone_number_id, from_, get_deleted_message(), is_private_on, is_unsafe_on)
        return

    if mssg.lower() == "private":
        if is_private_on:
            send_whatsapp_text_reply(phone_number_id, from_, "Private Mode is already ON", is_private_on, is_unsafe_on)
            return
        put_private_mode(from_, True, user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, get_private_mode_on_message(), is_private_on, is_unsafe_on)
        return
    
    if mssg.lower() == "unprivate":
        if not is_private_on:
            send_whatsapp_text_reply(phone_number_id, from_, "Private Mode is already OFF", is_private_on, is_unsafe_on)
            return
        if is_unsafe_on:
            send_whatsapp_text_reply(phone_number_id, from_, "Cannot turn off Private mode in Unsafe mode", is_private_on, is_unsafe_on)
            return
        put_private_mode(from_, False, user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, get_private_mode_off_message(), is_private_on, is_unsafe_on)
        return
    
    if mssg.lower() == "unsafe":
        if not allow_unsafe_mode:
            send_whatsapp_text_reply(phone_number_id, from_, "Sorry, Unsafe Mode is under development and not ready yet. Please try again later.", is_private_on, is_unsafe_on)
            return
        if is_unsafe_on:
            send_whatsapp_text_reply(phone_number_id, from_, "Unsafe Mode is already ON", is_private_on, is_unsafe_on)
            return
        put_unsafe_mode(from_, True, user_secret)
        put_private_mode(from_, True, user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, get_unsafe_mode_on_message(), is_private_on, is_unsafe_on)
        return
    
    if mssg.lower() == "safe":
        if not is_unsafe_on:
            send_whatsapp_text_reply(phone_number_id, from_, "Unsafe Mode is already OFF", is_private_on, is_unsafe_on)
            return
        put_unsafe_mode(from_, False, user_secret)
        put_private_mode(from_, False, user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, get_unsafe_mode_off_message(), is_private_on, is_unsafe_on)
        return
    
    if mssg.lower() == "i take responsibility":
        put_last_unsafe_accepted_timestamp(from_, int(time.time()), user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, "Thank you for accepting responsibility. You can now use unsafe mode.", is_private_on, is_unsafe_on)
        return

    if mssg.lower() == "about":
        send_whatsapp_text_reply(phone_number_id, from_, get_about_message(), is_private_on, is_unsafe_on)
        return

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

        return
    
    if mssg.lower() == "tweet":
        if is_unsafe_on or is_private_on:
                send_whatsapp_text_reply(phone_number_id, from_, tweet_disallowed_message(), is_private_on, is_unsafe_on)
                return
        
        history = get_short_term_memory(from_, user_secret)
        if(len(history) < 1):
            send_whatsapp_text_reply(phone_number_id, from_, "No existing history to tweet", is_private_on, is_unsafe_on)
            return
        last_message = history[-1]
        if last_message["role"] != "assistant":
            send_whatsapp_text_reply(phone_number_id, from_, "Last message not by assistant, not tweeting", is_private_on, is_unsafe_on)
            return
        tweet=last_message['message']

        last_found_tweet_id = None
        for msg in reversed(history):
            if msg['message'].find("https://x.com") != -1:
                match = re.search("status/(\d+)?s=", msg['message'])
                if match:
                    last_found_tweet_id = print(f"{match.group(0)}")
                    send_whatsapp_text_reply(phone_number_id, from_, found_tweet_context_message(last_found_tweet_id, msg['message']), is_private_on, is_unsafe_on)
                    break

        tweet_id=send_tweet(tweet, last_found_tweet_id)
        if tweet_id is None:
            send_whatsapp_text_reply(phone_number_id, from_, "Tweet failed", is_private_on, is_unsafe_on)
            return
        
        send_whatsapp_text_reply(phone_number_id, from_, "Tweeted [id:"+str(tweet_id)+"]: "+tweet, is_private_on, is_unsafe_on)
        return