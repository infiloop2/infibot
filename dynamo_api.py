import boto3
import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import re

prefix = os.environ.get('db_prefix')
if prefix == 'prod':
    prefix = ''

random_encryption_key = os.environ.get('random_encryption_key')

dynamodb = boto3.resource(
    'dynamodb',
    region_name= os.environ.get('aws_region_name'),
    aws_access_key_id=os.environ.get('aws_access_key_id'),
    aws_secret_access_key=os.environ.get('aws_secret_access_key'),
)
limit_table = dynamodb.Table(prefix+'infibot_quota')
short_term_history_table = dynamodb.Table(prefix+'infibot_short_term_history')
metadata_table = dynamodb.Table(prefix+'infibot_metadata')

def get_last_intro_message_timestamp(number, user_secret):
    attr_name = getSanitizedKey("last_intro_message_timestamp", user_secret) 
    try:
        k = getSanitizedKey(number, user_secret)
        return int(decrypt(user_secret, metadata_table.get_item(Key={'number': k})['Item'][attr_name]))
    except Exception as e:
        return 0
    
def put_last_intro_message_timestamp(number, timestamp, user_secret):
    attr_name = getSanitizedKey("last_intro_message_timestamp", user_secret) 
    k = getSanitizedKey(number, user_secret)
    metadata_table.update_item(
        Key={'number': k},
        UpdateExpression=f'SET {attr_name} = :val',
        ExpressionAttributeValues={
            ':val': encrypt(user_secret,str(timestamp))
        }
    )

def get_last_privacy_accepted_timestamp(number, user_secret):
    attr_name = getSanitizedKey("last_privacy_accepted_timestamp", user_secret) 
    try:
        k = getSanitizedKey(number, user_secret)
        return int(decrypt(user_secret, metadata_table.get_item(Key={'number': k})['Item'][attr_name]))
    except Exception as e:
        return 0
    
def put_last_privacy_accepted_timestamp(number, timestamp, user_secret):
    attr_name = getSanitizedKey("last_privacy_accepted_timestamp", user_secret) 
    k = getSanitizedKey(number, user_secret)
    metadata_table.update_item(
        Key={'number': k},
        UpdateExpression=f'SET {attr_name} = :val',
        ExpressionAttributeValues={
            ':val': encrypt(user_secret,str(timestamp))
        }
    )

def get_is_private_mode_on(number, user_secret):
    attr_name = getSanitizedKey("is_private_mode_on", user_secret) 
    try:
        k = getSanitizedKey(number, user_secret)
        return decrypt(user_secret, metadata_table.get_item(Key={'number': k})['Item'][attr_name]) == 'True'
    except Exception as e:
        return False

def put_private_mode(number, turn_on_private, user_secret):
    attr_name = getSanitizedKey("is_private_mode_on", user_secret) 
    k = getSanitizedKey(number, user_secret)
    metadata_table.update_item(
        Key={'number': k},
        UpdateExpression=f'SET {attr_name} = :val',
        ExpressionAttributeValues={
            ':val': encrypt(user_secret,str(turn_on_private))
        }
    )

def get_is_unsafe_mode_on(number, user_secret):
    attr_name = getSanitizedKey("is_unsafe_mode_on", user_secret) 
    try:
        k = getSanitizedKey(number, user_secret)
        return decrypt(user_secret, metadata_table.get_item(Key={'number': k})['Item'][attr_name]) == 'True'
    except Exception as e:
        return False

def put_unsafe_mode(number, turn_on_unsafe, user_secret):
    attr_name = getSanitizedKey("is_unsafe_mode_on", user_secret) 
    k = getSanitizedKey(number, user_secret)
    metadata_table.update_item(
        Key={'number': k},
        UpdateExpression=f'SET {attr_name} = :val',
        ExpressionAttributeValues={
            ':val': encrypt(user_secret,str(turn_on_unsafe))
        }
    )

def get_last_unsafe_accepted_timestamp(number, user_secret):
    attr_name = getSanitizedKey("last_unsafe_accepted_timestamp", user_secret) 
    try:
        k = getSanitizedKey(number, user_secret)
        return int(decrypt(user_secret, metadata_table.get_item(Key={'number': k})['Item'][attr_name]))
    except Exception as e:
        return 0
    
def put_last_unsafe_accepted_timestamp(number, timestamp, user_secret):
    attr_name = getSanitizedKey("last_unsafe_accepted_timestamp", user_secret) 
    k = getSanitizedKey(number, user_secret)
    metadata_table.update_item(
        Key={'number': k},
        UpdateExpression=f'SET {attr_name} = :val',
        ExpressionAttributeValues={
            ':val': encrypt(user_secret,str(timestamp))
        }
    )

def get_quota(number):
    try:
        return int(limit_table.get_item(Key={'number': number})['Item']['quota'])
    except Exception as e:
        return None

def put_quota(number, quota):
    limit_table.put_item(Item={'number': number, 'quota': str(quota)})

# Expected form:
# [{'timestamp': 123, 'role': "user", 'message': "hello"}, ... ]
def get_short_term_history(number, user_secret):
    try:
        k = getSanitizedKey(number, user_secret)
        data = short_term_history_table.get_item(Key={'number': k})['Item']['history']
        return json.loads(decrypt(user_secret, data))
    except Exception as e:
        return []
    
def put_short_term_history(number, history, user_secret):
    k = getSanitizedKey(number, user_secret)
    data = encrypt(user_secret,json.dumps(history))
    short_term_history_table.put_item(Item={'number': k, 'history': data})

def getSanitizedKey(k, user_secret):
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('', get_key(user_secret + k).decode())[-20:]

def get_key(str):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(str.encode())
    return base64.urlsafe_b64encode(digest.finalize())

def encrypt(password, str):
    if len(str) == 0:
        return ""
    f = Fernet(get_key(password+random_encryption_key))
    return f.encrypt(str.encode()).decode()

def decrypt(password, bts):
    if len(bts) == 0:
        return ""
    f = Fernet(get_key(password+random_encryption_key))
    return f.decrypt(bts).decode()