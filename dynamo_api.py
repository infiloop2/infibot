import boto3
import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

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

def get_quota(number):
    try:
        return int(limit_table.get_item(Key={'number': number})['Item']['quota'])
    except Exception as e:
        return None

def put_quota(number, quota):
    limit_table.put_item(Item={'number': number, 'quota': str(quota)})

# Expected form:
# [{'timestamp': 123, 'role': "user", 'message': "hello"}, ... ]
def get_short_term_history(number):
    try:
        data = short_term_history_table.get_item(Key={'number': number})['Item']['history']
        return json.loads(decrypt(number+random_encryption_key, data))
    except Exception as e:
        return []
    
def put_short_term_history(number, history):
    data = encrypt(number+random_encryption_key,json.dumps(history))
    short_term_history_table.put_item(Item={'number': number, 'history': data})


def get_key(str):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(str.encode())
    return base64.urlsafe_b64encode(digest.finalize())

def encrypt(password, str):
    if len(str) == 0:
        return ""
    f = Fernet(get_key(password))
    return f.encrypt(str.encode()).decode()

def decrypt(password, bts):
    if len(bts) == 0:
        return ""
    f = Fernet(get_key(password))
    return f.decrypt(bts).decode()