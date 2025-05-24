import string
import random
from datetime import datetime

def gen_custom_resume_id(prefix: str , length: int = 4) -> str:
    safe_prefix = prefix[:6].strip().upper().replace(" ", "")

    date = datetime.today().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{safe_prefix}-{date}-{random_suffix}"