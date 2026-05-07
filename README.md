# ⚽ eFootball Friend Match & League Bot

A high-performance Telegram bot designed for eFootball communities to manage Friend Match codes and organize automated leagues.

## 🚀 Main Features
- **Multi-language Support:** Somali (Default), English, and Arabic.
- **Challenge System:** Detects 8-digit room codes, prevents duplicates, and manages claims.
- **League System:** Automatic fixture generation for 4, 8, or 16 players.
- **Security:** Anti-flood, anti-spam, and admin-only controls.
- **24/7 Ready:** Optimized for Webhook deployment on Render, Railway, or VPS.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Library:** pyTelegramBotAPI (Telebot)
- **Database:** SQLite (Persistent Storage)
- **Web Framework:** Flask (for Webhooks)

## 📦 Setup & Installation
1. Clone the repo: `git clone https://github.com/USERNAME/REPO-NAME.git`
2. Install requirements: `pip install -r requirements.txt`
3. Configure `.env` with your `BOT_TOKEN` and `ADMIN_IDS`.
4. Run `python main.py`.

## 🛡️ Admin Commands
- `!stats` - View bot statistics.
- `!broadcast` - Send a message to all users.
- `!ban` / `!unban` - Manage user access.
