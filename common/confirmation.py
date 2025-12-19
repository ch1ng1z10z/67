import uuid
from .redis import redis_client

def save_code(user_id):
    code = str(uuid.uuid4())[:6]
    redis_client.setex(f"confirm:{user_id}", 300, code)
    return code

def verify_code(user_id, code):
    key = f"confirm:{user_id}"
    saved = redis_client.get(key)

    if saved == code:
        redis_client.delete(key)
        return True
    return False
