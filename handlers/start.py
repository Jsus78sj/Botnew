# ============================================================
#Group Manager Bot
# Author: LearningBotsOfficial (https://github.com/LearningBotsOfficial) 
# Support: https://t.me/LearningBotsCommunity
# Channel: https://t.me/learning_bots
# YouTube: https://youtube.com/@learning_bots
# License: Open-source (keep credits, no resale)
# ============================================================


from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto
)
from config import BOT_USERNAME, SUPPORT_GROUP, UPDATE_CHANNEL, START_IMAGE, OWNER_ID
import db

def register_handlers(app: Client):

# ==========================================================
# Start Message
# ==========================================================
    async def send_start_menu(message, user):
        text = f"""

   ✨ أهلاً {user}! ✨

👋 أنا Nomad 🤖 

المميزات:
─────────────────────────────
- حماية ذكية من السبام والروابط
- نظام قفل متكيّف (روابط، ميديا، لغة وأكثر)
- حماية معيارية وقابلة للتوسع
- واجهة أنيقة بأزرار تفاعلية

» المزيد من المميزات قريباً ...
"""

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚒️ أضفني للمجموعة ⚒️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [
                InlineKeyboardButton("⌂ الدعم ⌂", url=SUPPORT_GROUP),
                InlineKeyboardButton("⌂ التحديثات ⌂", url=UPDATE_CHANNEL),
            ],
            [
                InlineKeyboardButton("※ ŎŴɳēŔ ※", url=f"tg://user?id={OWNER_ID}"),
                InlineKeyboardButton("Repo", url="https://github.com/LearningBotsOfficial/Nomade"),
                
            ],
            [InlineKeyboardButton("📚 قائمة الأوامر 📚", callback_data="help")]
        ])

        # If /start command, send a new photo
        if message.text:
            await message.reply_photo(START_IMAGE, caption=text, reply_markup=buttons)
        else:
            # If callback, edit the same message
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await message.edit_media(media=media, reply_markup=buttons)

# ==========================================================
# Start Command
# ==========================================================
    @app.on_message(filters.private & filters.command("start", prefixes=[""]))
    async def start_command(client, message):
        user = message.from_user
        await db.add_user(user.id, user.first_name)
        await send_start_menu(message, user.first_name)

# ==========================================================
# Help Menu Message
# ==========================================================
    async def send_help_menu(message):
        text = """
╔══════════════════╗
   قائمة المساعدة
╚══════════════════╝

اختر فئة لاستعراض الأوامر:
─────────────────────────────
"""
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⌂ الترحيب ⌂", callback_data="greetings"),
                InlineKeyboardButton("⌂ الأقفال ⌂", callback_data="locks"),
            ],
            [
                InlineKeyboardButton("⌂ الإدارة ⌂", callback_data="moderation")
            ],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")]
        ])

        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await message.edit_media(media=media, reply_markup=buttons)

# ==========================================================
# Help Callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("help"))
    async def help_callback(client, callback_query):
        await send_help_menu(callback_query.message)
        await callback_query.answer()

# ==========================================================
# back to start Callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("back_to_start"))
    async def back_to_start_callback(client, callback_query):
        user = callback_query.from_user.first_name
        await send_start_menu(callback_query.message, user)
        await callback_query.answer()

# ==========================================================
# Greetings Callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("greetings"))
    async def greetings_callback(client, callback_query):
        text = """
╔══════════════════╗
    ⚙ نظام الترحيب
╚══════════════════╝

أوامر إدارة رسائل الترحيب:

- تعيينترحيب <نص> : تعيين رسالة ترحيب مخصصة
- ترحيب on      : تفعيل رسائل الترحيب
- ترحيب off     : إيقاف رسائل الترحيب

المتغيرات المدعومة:
- {username}   : اسم المستخدم
- {first_name} : الاسم الأول
- {mention}    : ذكر المستخدم
- {title}      : اسم المجموعة

مثال:
 تعيينترحيب أهلاً {first_name}! مرحباً بك في {title}!
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data="help")]
        ])
        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

# ==========================================================
# Locks callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("locks"))
    async def locks_callback(client, callback_query):
        text = """
╔══════════════════╗
     ⚙ نظام الأقفال
╚══════════════════╝

أوامر إدارة الأقفال:

- قفل <نوع>    : تفعيل قفل في المجموعة
- فتح <نوع>  : إلغاء قفل في المجموعة
- locks         : عرض الأقفال النشطة حالياً

أنواع الأقفال المتاحة:
- url      : حجب الروابط
- sticker  : حجب الستيكرات
- media    : حجب الصور والفيديو
- username : حجب رسائل تحتوي على @mentions
- forward  : حجب الرسائل المعاد توجيهها

مثال:
 قفل url     : يحجب أي رسالة تحتوي رابطاً
 فتح sticker : يسمح بالستيكرات مرة أخرى
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data="help")]
        ])
        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

# ==========================================================
# Moderation Callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("moderation"))
    async def info_callback(client, callback_query):
        try:
            text = """
╔══════════════════╗
      ⚙️ نظام الإدارة
╚══════════════════╝

أدِر مجموعتك بسهولة باستخدام:

¤ طرد <مستخدم>       — طرد عضو
¤ حظر <مستخدم>        — حظر دائم
¤ الغاء حظر <مستخدم>      — رفع الحظر
¤ كتم <مستخدم>       — كتم العضو
¤ الغاء كتم <مستخدم>     — رفع الكتم
¤ تحذير <مستخدم>       — تحذير (3 = كتم)
¤ تحذيرات <مستخدم>      — عرض التحذيرات
¤ resetتحذيرات <مستخدم> — مسح التحذيرات
¤ ترقية <مستخدم>    — ترقية لأدمن
¤ تنزيل <مستخدم>     — إزالة من الأدمن

💡 مثال:
رد على مستخدم أو اكتب
<code>حظر @username</code>

"""
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="help")]
            ])
    
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
    
        except Exception as e:
            print(f"Error in info_callback: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)
    

# ==========================================================
# Broadcast Command
# ==========================================================
    @app.on_message(filters.private & filters.command("بث", prefixes=[""]))
    async def broadcast_message(client, message):
        if not message.reply_to_message:
            await message.reply_text("⚠️ يرجى الرد على رسالة لبثها.")
            return

        if message.from_user.id != OWNER_ID:
            await message.reply_text("❌ هذا الأمر للمالك فقط.")
            return

        text_to_send = message.reply_to_message.text or message.reply_to_message.caption
        if not text_to_send:
            await message.reply_text("⚠️ الرسالة التي رددت عليها لا تحتوي نصاً.")
            return

        users = await db.get_all_users()
        sent, failed = 0, 0

        await message.reply_text(f"جارٍ الإرسال إلى {len(users)} مستخدم..")

        for user_id in users:
            try:
                await client.send_message(user_id, text_to_send)
                sent += 1
            except Exception:
                failed += 1

        await message.reply_text(f"✅ اكتمل البث!\n\nأُرسل: {sent}\nفشل: {failed}")

# ==========================================================
# stats Command
# ==========================================================
    @app.on_message(filters.private & filters.command("احصاء", prefixes=[""]))
    async def stats_command(client, message):
        if message.from_user.id != OWNER_ID:
            return await message.reply_text("❌ هذا الأمر للمالك فقط")

        users = await db.get_all_users()
        return await message.reply_text(f"💡 إجمالي المستخدمين: {len(users)}")
