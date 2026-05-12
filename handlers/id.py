import random, re, time, os
from threading import Thread
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from handlers.Ranks import *                       # تم التصحيح
from handlers.utils import get_creation_date      # تم التصحيح (تأكد من وجودها في utils.py)
from pyrogram.raw.functions.users import GetFullUser
from io import BytesIO
from pyrogram.file_id import FileId, FileType, ThumbnailSource
from pyrogram.raw.functions.channels import GetFullChannel
from handlers.games import get_emoji_bank
from handlers.Ranks import isLockCommand           # تم التصحيح
from bot import app

# ... (باقي الكود الأصلي بدون تعديل، ابدأ من المتغيرات custom_ids...)
