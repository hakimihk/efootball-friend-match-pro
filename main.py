import telebot
import json
import os
from telebot import types
import database as db
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

def get_text(key, user_id):
    lang = db.get_user_lang(user_id) or 'so'
    try:
        with open(f'locales/{lang}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(key, f"Missing key: {key}")
    except:
        return f"Error: {key}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    db.register_user(user_id, message.from_user.username)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(get_text('challenge', user_id), callback_data="challenge"),
        types.InlineKeyboardButton(get_text('league', user_id), callback_data="league"),
        types.InlineKeyboardButton(get_text('help', user_id), callback_data="help"),
        types.InlineKeyboardButton(get_text('settings', user_id), callback_data="settings")
    )
    
    bot.send_message(message.chat.id, f"⚽ {get_text('welcome_title', user_id)}\n\n{get_text('welcome_desc', user_id)}", reply_markup=markup)

@bot.message_handler(func=lambda m: len(m.text) == 8 and m.text.isdigit())
def handle_code(message):
    user_id = message.from_user.id
    code = message.text
    
    if db.is_duplicate_code(code):
        bot.reply_to(message, "⚠️ Sxb code-kan mar hore ayaa la soo geliyay!")
        return

    db.register_code(code, user_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(get_text('claim', user_id), callback_data=f"claim_{code}"))
    
    user_name = message.from_user.username if message.from_user.username else message.from_user.first_name
    msg = f"🎮 **NEW CHALLENGE!**\n\nCode: `{code}`\nUser: @{user_name}\n\n{get_text('room_instruction', user_id)}"
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.from_user.id
    try:
        if call.data == "challenge":
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Soo dir 8-da lambar ee Room Code-ka ah 🎮")

        elif call.data.startswith("claim_"):
            code = call.data.split("_")[1]
            db.claim_code(code, user_id)
            bot.answer_callback_query(call.id, text=get_text('code_claimed', user_id))
            bot.send_message(call.message.chat.id, f"✅ {get_text('start_match', user_id)}")
            
        elif call.data == "settings":
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, get_text('select_lang', user_id))
    except Exception as e:
        bot.answer_callback_query(call.id, text="Cillad baa dhacday!")

if __name__ == "__main__":
    db.init_db()
    print("Bot-ka waa la kiciyay (Polling)...")
    bot.remove_webhook()
    bot.infinity_polling()
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
