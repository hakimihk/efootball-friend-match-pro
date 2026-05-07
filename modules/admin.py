from config import ADMIN_IDS
import database as db

def is_admin(user_id):
    return user_id in ADMIN_IDS

def get_stats():
    total_users = db.count_users()
    active_leagues = db.count_active_leagues()
    return f"📊 **Statistics**\n\nTotal Users: {total_users}\nActive Leagues: {active_leagues}"

def broadcast_message(bot, text):
    users = db.get_all_users()
    count = 0
    for user in users:
        try:
            bot.send_message(user[0], text)
            count += 1
        except:
            continue
    return count
