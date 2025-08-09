from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

with open('/home/neooo333/Projects/telegram_key.txt', 'r') as key:
    key_file = key.read ().strip ()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your friendly bot.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send /start to get a greeting!')

if __name__ == '__main__':
    app = ApplicationBuilder().token(key_file).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is running...")
    app.run_polling()
