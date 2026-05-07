import re
from database import is_duplicate_code, register_code

def validate_room_code(text):
    # Wuxuu hubinayaa inay tahay 8 lambar oo kaliya
    return bool(re.match(r'^\d{8}$', text))

def process_new_code(code, user_id):
    if is_duplicate_code(code):
        return False
    register_code(code, user_id)
    return True
