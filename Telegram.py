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
        "1. /start - send greeting!\n"
        "2. /help - calls command menu\n"
        "3. /exchange - calls for exchnge market function for a specified security\n"
        "4. /pe_qqq - returns 5 NASDAQ stocks with lowest PE\n"
        "4. /pe_snp - returns 5 SNP 500 stocks with lowest PE\n"
)

async def pe_qqq(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text ('Loading data...')
    five_stocks = ff.pe_qqq ()
    message = (
        f"1. {five_stocks.index[0]} | PE: {five_stocks.iloc[0]['PE']} | Dividends: {five_stocks.iloc[0]['DIV']}\n"
        f"2. {five_stocks.index[1]} | PE: {five_stocks.iloc[1]['PE']} | Dividends: {five_stocks.iloc[1]['DIV']}\n"
        f"3. {five_stocks.index[2]} | PE: {five_stocks.iloc[2]['PE']} | Dividends: {five_stocks.iloc[2]['DIV']}\n"
        f"4. {five_stocks.index[3]} | PE: {five_stocks.iloc[3]['PE']} | Dividends: {five_stocks.iloc[3]['DIV']}\n"
        f"5. {five_stocks.index[4]} | PE: {five_stocks.iloc[4]['PE']} | Dividends: {five_stocks.iloc[4]['DIV']}"
    )
    await update.message.reply_text (message)

async def pe_snp (update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text ('Loading Data...')
    snp_data_five = ff.pe_snp ()
    message = (
        f"1. {snp_data_five.index[0]} | PE: {snp_data_five.iloc[0]['PE']} | Dividends: {snp_data_five.iloc[0]['DIV']}\n"
        f"2. {snp_data_five.index[1]} | PE: {snp_data_five.iloc[1]['PE']} | Dividends: {snp_data_five.iloc[1]['DIV']}\n"
        f"3. {snp_data_five.index[2]} | PE: {snp_data_five.iloc[2]['PE']} | Dividends: {snp_data_five.iloc[2]['DIV']}\n"
        f"4. {snp_data_five.index[3]} | PE: {snp_data_five.iloc[3]['PE']} | Dividends: {snp_data_five.iloc[3]['DIV']}\n"
        f"5. {snp_data_five.index[4]} | PE: {snp_data_five.iloc[4]['PE']} | Dividends: {snp_data_five.iloc[4]['DIV']}"
    )
    await update.message.reply_text (message)


########################################conversation for the exchange ##############################################################

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


####################################################################################



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
    app.add_handler(CommandHandler("pe_qqq", pe_qqq))
    app.add_handler(CommandHandler("pe_snp", pe_snp))

    print("Bot is running...")
    app.run_polling()
