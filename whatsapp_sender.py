import requests
import os
import json

def send_whatsapp_text_reply(phone_number_id, to, reply_message, is_private_on, is_unsafe_on):
    body_text = reply_message
    prefix = ""
    if is_private_on:
        prefix = prefix + "🔒Private Mode ON:"
    if is_unsafe_on:
        prefix = prefix + "💀Unsafe Mode ON:"
    
        body_text = f"""{prefix}
{body_text}
        """
    json_data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": body_text},
    }
    data = json.dumps(json_data)
    url = f"https://graph.facebook.com/v16.0/{phone_number_id}/messages"
    headers = {
        'Authorization': f"Bearer {os.environ.get('whatsapp_token')}",
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()

def send_whatsapp_image_reply(phone_number_id, to, image_url):
    json_data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": {"link": image_url},
    }
    data = json.dumps(json_data)
    url = f"https://graph.facebook.com/v16.0/{phone_number_id}/messages"
    headers = {
        'Authorization': f"Bearer {os.environ.get('whatsapp_token')}",
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()