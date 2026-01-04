import asyncio
from datetime import time
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram import Update

TOKEN = "8489609878:AAG9PV67-CGuiOiA6p-j95sCxbhIhsAx358"
GROUP_CHAT_ID = -5227660132  # Replace with your group ID
REASK_INTERVAL = 600  # 10 minutes in seconds

waiting_for_yes = False


async def ask_task(context: ContextTypes.DEFAULT_TYPE):
    global waiting_for_yes
    waiting_for_yes = True
    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Derti l Yasser Flexotide oGhseltilih snano ?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for_yes

    if update.effective_chat.id != GROUP_CHAT_ID:
        return

    if waiting_for_yes:
        text = update.message.text.lower().strip()

        if text == "Ah":
            waiting_for_yes = False
            await update.message.reply_text("Great! See you next time.")
        else:
            await update.message.reply_text("I'll ask again in 10 minutes.")
            await asyncio.sleep(REASK_INTERVAL)
            await ask_task(context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Reminder bot is running.")


async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Listen for replies
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Schedule daily reminders
    app.job_queue.run_daily(ask_task, time(hour=9, minute=0))
    app.job_queue.run_daily(ask_task, time(hour=19, minute=0))

    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
