import json

def get_text(key, lang_code='so'):
    try:
        with open(f'locales/{lang_code}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(key, f"Missing key: {key}")
    except FileNotFoundError:
        return f"Language {lang_code} not found."

def get_main_keyboard(lang):
    from telebot import types
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(f"🎮 {get_text('challenge', lang)}", callback_data="challenge"),
        types.InlineKeyboardButton(f"🎲 {get_text('league', lang)}", callback_data="league"),
        types.InlineKeyboardButton(f"📖 {get_text('help', lang)}", callback_data="help"),
        types.InlineKeyboardButton(f"⚙️ {get_text('settings', lang)}", callback_data="settings")
    )
    return markup
