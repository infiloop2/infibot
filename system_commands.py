from whatsapp_sender import send_whatsapp_text_reply
from system_messages import get_fresh_message, get_quota_left_message, get_deleted_message, get_capabilities_message, get_privacy_message, get_about_message
from dynamo_api import get_quota
from short_term_memory import write_short_term_memory

def is_system_command(mssg):
    if mssg.lower() == "help":
        return True
    if mssg.lower() == "quota":
        return True
    if mssg.lower() == "examples":
        return True 
    if mssg.lower() == "privacy":
        return True 
    if mssg.lower() == "accept privacy":
        return True 
    if mssg.lower() == "history":
        return True 
    if mssg.lower() == "delete":
        return True 
    if mssg.lower() == "private":
        return True 
    if mssg.lower() == "about":
        return True 
    return False
    
def handle_system_command(mssg, phone_number_id, from_, user_secret):
    if mssg.lower() == "help":
        send_whatsapp_text_reply(phone_number_id, from_, get_fresh_message(get_quota(from_)))
        return

    if mssg.lower() == "quota":
        send_whatsapp_text_reply(phone_number_id, from_, get_quota_left_message(get_quota(from_)))
        return

    if mssg.lower() == "examples":
        send_whatsapp_text_reply(phone_number_id, from_, get_capabilities_message())
        return

    if mssg.lower() == "privacy":
        send_whatsapp_text_reply(phone_number_id, from_, get_privacy_message())
        return

    if mssg.lower() == "delete":
        write_short_term_memory(from_, [], user_secret)
        send_whatsapp_text_reply(phone_number_id, from_, get_deleted_message())
        return

    if mssg.lower() == "about":
        send_whatsapp_text_reply(phone_number_id, from_, get_about_message())
        return