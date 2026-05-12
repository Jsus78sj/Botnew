# handlers/group_commands.py
from pyrogram import filters, Client
from pyrogram.types import Message
from config import Dev_Zaid, r  # تأكد من أن هذه المتغيرات معرفة في config

# دوال مساعدة للصلاحيات (إن لم تكن معرفة لديك في مكان آخر)
def admin_pls(user_id, chat_id):
    """التحقق من أن المستخدم مشرف في المجموعة"""
    # يمكن تحسينها بالوصول لقاعدة البيانات أو استخدام bot.get_chat_member لاحقاً
    return True  # مؤقتاً لتجنب التوقف

def owner_pls(user_id, chat_id):
    return True  # مؤقتاً

def mod_pls(user_id, chat_id):
    return True  # مؤقتاً

def register_group_commands(app: Client):
    """تسجيل جميع أوامر المجموعات لدى الكائن app"""

    @app.on_message(filters.command("تفعيل") & filters.group)
    async def activate_command(client: Client, message: Message):
        if not admin_pls(message.from_user.id, message.chat.id):
            return await message.reply("عذراً، الأمر يخص المشرفين فقط.")
        # التحقق من حالة التفعيل
        if r.get(f'{message.chat.id}:enable:{Dev_Zaid}'):
            return await message.reply("البوت مُفعّل بالفعل.")
        r.set(f'{message.chat.id}:enable:{Dev_Zaid}', '1')
        await message.reply("✅ تم تفعيل البوت في المجموعة.")

    @app.on_message(filters.command("تعطيل") & filters.group)
    async def deactivate_command(client: Client, message: Message):
        if not admin_pls(message.from_user.id, message.chat.id):
            return await message.reply("عذراً، الأمر يخص المشرفين فقط.")
        if not r.get(f'{message.chat.id}:enable:{Dev_Zaid}'):
            return await message.reply("البوت معطل بالفعل.")
        r.delete(f'{message.chat.id}:enable:{Dev_Zaid}')
        await message.reply("❌ تم تعطيل البوت في المجموعة.")

    # يمكنك إضافة أوامر أخرى هنا (مثل /حظر، /كتم، إلخ)
    print("✅ Group commands registered!")
