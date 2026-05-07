import telebot
from flask import Flask, request
from config import TOKEN, WEBHOOK_URL, PORT
import database as db
from utils.helpers import get_main_keyboard, get_text
from modules import admin, challenge, settings
from utils import security

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

# --- WEBHOOK SETUP ---
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + TOKEN)
    return "Bot is Running!", 200

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    # Register user in DB if not exists
    db.add_user(user_id, message.from_user.username)
    lang = db.get_user_lang(user_id)
    
    welcome_msg = f"⚽ <b>{get_text('welcome_title', lang)}</b>\n\n{get_text('welcome_desc', lang)}"
    bot.send_message(message.chat.id, welcome_msg, reply_markup=get_main_keyboard(lang))

# --- ROOM CODE DETECTION (CHALLENGE SYSTEM) ---
@bot.message_handler(func=lambda m: len(m.text) == 8 and m.text.isdigit())
def handle_room_code(message):
    lang = db.get_user_lang(message.from_user.id)
    code = message.text
    
    # Anti-spam check
    if db.is_duplicate_code(code):
        bot.delete_message(message.chat.id, message.message_id)
        return

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(f"📥 {get_text('claim', lang)}", callback_data=f"claim_{code}_{message.from_user.id}"))
    
    msg = f"🎮 <b>NEW CHALLENGE!</b>\n\nCode: <code>{code}</code>\nUser: @{message.from_user.username}\n\n<i>{get_text('room_instruction', lang)}</i>"
    bot.send_message(message.chat.id, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('claim_'))
def claim_code(call):
    _, code, owner_id = call.data.split('_')
    user_id = call.from_user.id
    lang = db.get_user_lang(user_id)

    if str(user_id) == owner_id:
        bot.answer_callback_query(call.id, get_text('cant_claim_own', lang), show_alert=True)
        return

    db.mark_code_claimed(code, user_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ <b>Code Claimed!</b>\n\nCode: <code>{code}</code>\nClaimed by: @{call.from_user.username}",
        reply_markup=None
    )

if __name__ == "__main__":
    db.init_db()
    print("Bot-ka waa la kiciyay (Polling Mode)...")
    bot.remove_webhook()
    bot.infinity_polling()
