from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
import finance_functions as ff

with open('telegram_key.txt', 'r') as key:
    key_file = key.read ().strip ()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user ['first_name']
    await update.message.reply_text(f'Hello {user}! I am your friendly bot.')



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""
1. /start - send greeting!
2. /help - calls command menu 
""")
    

TICKER = 0

async def exchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'I will get you Stock Exchange Info. Text ticker:')
    return TICKER

async def exchange_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    company = update.message.text  # Get user input
    exchanges = ff.exchange_name(company)  # Call your function

    if exchanges:
        await update.message.reply_text(f"Exchanges for {company}: {', '.join(exchanges)}")
    else:
        await update.message.reply_text(f"No exchange info found for {company}.")

    return ConversationHandler.END 

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Conversation cancelled.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(key_file).build()

  

    conv_exchange = ConversationHandler(
    entry_points=[CommandHandler("exchange", exchange)],
    states={
        TICKER: [MessageHandler(filters.TEXT & ~filters.COMMAND, exchange_name_handler)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
    

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(conv_exchange) 


    print("Bot is running...")
    app.run_polling()
