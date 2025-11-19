from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import os

TOKEN = os.environ.get("TOKEN")
OWNER_USERNAME = "u_3_cc"  # ضع هنا اسم المستخدم الخاص بك بدون @

# المتغيرات لتخزين الكود
current_code = ""
code_status = "❌ لا يوجد كود حالياً"
current_link = ""

# رسالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = f"""
مرحباً بك في بوت أكواد أمازون! 🛍️

🔍 لعرض الكود الحالي:
أرسل كلمة: كود

📝 لتحديث الكود (خاص بالمالك {OWNER_USERNAME}):
أرسل الكود متبوعًا بالحالة والرابط، مثال:
6OOR2 صالحة https://amzn.to/4oJKpUi
"""
    await update.message.reply_text(welcome_message)

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_code, code_status, current_link
    text = update.message.text.strip()
    username = update.message.from_user.username  # اسم المستخدم الذي أرسل الرسالة

    if text == "كود":
        if current_code and current_link:
            message = f"""
🔹 احذفوا المنتجات اللي بسلتكم
🔹 وارجعوا ضيفوها من رابطي عشان توصلني العمولة وتستفيدوا من الخصم 
[الكود أمانه عندك لاستخدامك انت فقط ]
🕒 الكود شغال لفترة محدودة! لا يفوتكم 👇

📦 الكود: {current_code}
🔗 الرابط: {current_link}
حالة الكود: {code_status}
"""
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("❌ لا يوجد كود حاليا.")
    else:
        if username == OWNER_USERNAME:
            # الرسالة تتكون من: الكود + الحالة + الرابط
            parts = text.split(maxsplit=2)
            if len(parts) < 3:
                await update.message.reply_text("❌ الرجاء إرسال الكود + الحالة + الرابط، مثال:\n6OOR2 صالحة https://amzn.to/4oJKpUi")
                return

            current_code = parts[0]
            code_status = parts[1]
            current_link = parts[2]

            await update.message.reply_text(f"✔️ تم تحديث الكود بنجاح!\nالكود: {current_code}\nالحالة: {code_status}\nالرابط: {current_link}")
        else:
            await update.message.reply_text("❌ عذراً، لا يمكنك تحديث الكود.")

# إنشاء التطبيق
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
