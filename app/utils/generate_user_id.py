import random
import string

def generate_user_id():
    prefix = "USR"
    suffix = ''.join(random.choices(string.digits, k=4))  
    custom_id = f"{prefix}-{suffix}"
    return custom_id