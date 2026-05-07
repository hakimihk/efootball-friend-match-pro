from telebot import types

def language_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🇸🇴 Somali", callback_data="set_so"),
        types.InlineKeyboardButton("🇺🇸 English", callback_data="set_en"),
        types.InlineKeyboardButton("🇸🇦 Arabic", callback_data="set_ar")
    )
    return markup
