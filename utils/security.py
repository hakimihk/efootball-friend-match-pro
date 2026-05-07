import time

user_last_msg = {}

def is_flooding(user_id):
    current_time = time.time()
    last_time = user_last_msg.get(user_id, 0)
    
    if current_time - last_time < 2:  # 2 second cooldown
        return True
    
    user_last_msg[user_id] = current_time
    return False
