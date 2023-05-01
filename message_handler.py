import time
import os
from system_messages import get_fresh_message, under_quota_message, too_long_message
from rate_limits import is_within_limits, reset_limits, use_one_limit
from short_term_memory import get_short_term_memory, write_short_term_memory, append_history
from openai_api import get_openai_response
from dynamo_api import get_quota, get_last_intro_message_timestamp, put_last_intro_message_timestamp
from commands import handle_command
from whatsapp_sender import send_whatsapp_text_reply
from system_commands import is_system_command, handle_system_command

# Handle text messages to phone number ID, from, timestamp with message body
def handle_text_message(phone_number_id, from_, timestamp, message, user_secret):
    current_time = int(time.time())
    if current_time - timestamp > 60:
        return
    
    if from_ == os.environ.get("admin_phone_number"):
        # admin system messages
        if message.startswith("Quota"):
            spl = message.split(" ")
            if len(spl) == 4:
                if spl[3] != os.environ.get("admin_password"):
                    send_whatsapp_text_reply(phone_number_id, from_, "Invalid admin password")
                    return
                reset_limits(spl[1], spl[2])
                send_whatsapp_text_reply(phone_number_id, from_, "Quota reset for " + spl[1] + " to " + str(spl[2]))
                return
    
    # Check if within limits
    if not is_within_limits(from_):
        send_whatsapp_text_reply(phone_number_id, from_, under_quota_message(from_))
        return
    use_one_limit(from_)
    
    if len(message) > 2000:
        send_whatsapp_text_reply(phone_number_id, from_, too_long_message())
        return
        
    # Handle system messages from users
    if is_system_command(message):
        handle_system_command(message, phone_number_id, from_, user_secret)
        return

    history = get_short_term_memory(from_, user_secret)
    if len(history) == 0:
        # Send welcome message if not sent within last 6 hours already
        last_ts = get_last_intro_message_timestamp(from_, user_secret)
        if current_time - last_ts > 6 * 3600:
            send_whatsapp_text_reply(phone_number_id, from_, get_fresh_message(get_quota(from_)))
            put_last_intro_message_timestamp(from_, current_time, user_secret)

    ai_response, command = get_openai_response(message, history)
    
    #Send assistant reply
    send_whatsapp_text_reply(phone_number_id, from_, ai_response)
    # Append to history
    history = append_history(history, "user", message)
    history = append_history(history, "assistant", ai_response)
    write_short_term_memory(from_, history, user_secret)
        
   
    if command is not None:
        handle_command(command, phone_number_id, from_, history, user_secret)