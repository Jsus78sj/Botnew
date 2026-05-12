# bot.py — shared Pyrogram Client instance
# All handlers import `app` from here
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "group_manager_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
