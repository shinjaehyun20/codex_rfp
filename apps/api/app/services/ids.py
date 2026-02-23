import random
import string

def make_id(prefix: str) -> str:
    token = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{token}"
