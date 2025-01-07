import random
import string

def generate_history_id():
    prefix = "HIS"
    suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}-{suffix}"