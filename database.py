import sqlite3

DB_NAME = "efootball.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, lang TEXT DEFAULT 'so')''')
    c.execute('''CREATE TABLE IF NOT EXISTS codes (code TEXT PRIMARY KEY, owner_id INTEGER, claimed_by INTEGER DEFAULT NULL)''')
    conn.commit()
    conn.close()

def get_user_lang(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT lang FROM users WHERE user_id=?", (user_id,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else 'so'

def register_user(user_id, username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def is_duplicate_code(code):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM codes WHERE code=?", (code,))
    res = c.fetchone()
    conn.close()
    return res is not None

def register_code(code, owner_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO codes (code, owner_id) VALUES (?, ?)", (code, owner_id))
    conn.commit()
    conn.close()

def claim_code(code, user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE codes SET claimed_by=? WHERE code=?", (user_id, code))
    conn.commit()
    conn.close()
