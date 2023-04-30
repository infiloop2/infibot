import requests
import os
import json

def send_whatsapp_text_reply(phone_number_id, to, reply_message):
    json_data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": reply_message},
    }
    data = json.dumps(json_data)
    url = f"https://graph.facebook.com/v16.0/{phone_number_id}/messages"
    headers = {
        'Authorization': f"Bearer {os.environ.get('whatsapp_token')}",
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        print("Error:", error)

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

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        print("Error:", error)