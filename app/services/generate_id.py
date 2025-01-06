import random
import string

def generate_id(category: str):
    prefix = "END" if category == "diabetes" else "PSIQ" if category == "psiquiatria" else "GEN"
    suffix = ''.join(random.choices(string.digits, k=4))  
    custom_id = f"{prefix}-{suffix}"
    return custom_id