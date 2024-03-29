import json
import os
import hmac
import hashlib
from message_handler import handle_text_message
from whatsapp_sender import send_whatsapp_text_reply
from system_messages import system_error_message, system_admin_message

def lambda_handler(event, context):
    # Handle GET requests for subscription verification
    if event.get("requestContext", {}).get("http", {}).get("method") == "GET":
        queryParams = event.get("queryStringParameters")
        if queryParams:
            mode = queryParams.get("hub.mode")
            if mode == "subscribe":
                verifyToken = queryParams.get("hub.verify_token")
                if verifyToken == os.environ.get("whatsapp_webhook_secret"):
                    challenge = queryParams.get("hub.challenge")
                    return {
                        "statusCode": 200,
                        "body": int(challenge),
                        "isBase64Encoded": False
                    }
                else:
                    responseBody = "Error, wrong validation token"
                    return {
                        "statusCode": 403,
                        "body": json.dumps(responseBody),
                        "isBase64Encoded": False
                    }
            else:
                responseBody = "Error, wrong mode"
                return {
                    "statusCode": 403,
                    "body": json.dumps(responseBody),
                    "isBase64Encoded": False
                }
        else:
            responseBody = "Error, no query parameters"
            return {
                "statusCode": 403,
                "body": json.dumps(responseBody),
                "isBase64Encoded": False
            }
    # Handle POST requests for incoming messages
    elif event.get("requestContext", {}).get("http", {}).get("method") == "POST":
        body = json.loads(event["body"])
        entries = body["entry"]
        for entry in entries:
            for change in entry["changes"]:
                value = change["value"]
                if value is not None:
                    display_phone_number = value["metadata"]["display_phone_number"]
                    phone_number_id = value["metadata"]["phone_number_id"]
                    if display_phone_number != os.environ.get('bot_phone_number'):
                        continue
                    if value.get("messages") is not None:
                        for message in value["messages"]:
                            if message["type"] == "text":
                                # Only handling text messages
                                from_ = message["from"]
                                timestamp = int(message['timestamp'])
                                message_body = message["text"]["body"]
                                if from_ != os.environ.get("admin_phone_number"):
                                    send_whatsapp_text_reply(phone_number_id, from_, system_admin_message(), is_private_on=False, is_unsafe_on=False)
                                    return {
                                        "statusCode": 200,
                                        "body": json.dumps("Done"),
                                        "isBase64Encoded": False
                                    }
                                try:
                                    handle_text_message(phone_number_id, from_, timestamp, message_body, getUserEncryptionSecret(event, from_))
                                except Exception as e:
                                    print(f"An exception occurred: {e}")
                                    send_whatsapp_text_reply(phone_number_id, from_, system_error_message(), is_private_on=False, is_unsafe_on=False)
                                return {
                                    "statusCode": 200,
                                    "body": json.dumps("Done"),
                                    "isBase64Encoded": False
                                }
    else:
        responseBody = "Unsupported method"
        return {
            "statusCode": 403,
            "body": json.dumps(responseBody),
            "isBase64Encoded": False
        }

    return None

def getUserEncryptionSecret(event, from_):
    # Not purely a user defined secret, but derived from aws parameters so as not to be
    # predictable by admin
    domainContext = event["requestContext"]["domainPrefix"]
    userAgent = event["requestContext"]["http"]["userAgent"]
    # Do not add timestamp as that changes the keys for each message
    #unixTimestamp = int(event["requestContext"]["timeEpoch"])
    #unixTimestamp = unixTimestamp - (unixTimestamp % 86400000) # Round down to nearest day
    return str(domainContext)+str(userAgent)+str(from_)

def verify_webhook(event):
    signature = event["headers"]["x-hub-signature-256"]
    elements = signature.split("=")
    signatureHash = elements[1]

    key = os.environ.get("whatsapp_webhook_secret").encode()
    payload = event['body'].encode()
    calculatedHash = hmac.new(key, payload, digestmod=hashlib.sha256).hexdigest()
    
    return signatureHash != calculatedHash