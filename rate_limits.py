from dynamo_api import get_quota, put_quota

def is_within_limits(number):
    quota = get_quota(number)
    if quota is None:
        return False
    else:
        return quota > 0
    
def reset_limits(number, limit):
    put_quota(number, limit)

def use_one_limit(number):
    quota = get_quota(number)
    if quota is None:
        return False
    else:
        put_quota(number, quota - 1)
        return True