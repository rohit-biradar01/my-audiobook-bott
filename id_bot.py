import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Load environment variables from a .env file for local testing
load_dotenv()

# --- Configuration ---
TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found. Make sure you have a .env file for local testing.")

# --- !!! YOUR AUDIOBOOK CATALOG GOES HERE !!! ---
# Replace the examples below with your actual book titles and file_ids.
# Use all lowercase for the book titles.
AUDIOBOOK_CATALOG = {
   "Harry Potter Book 1": "BQACAgUAAxkBAAEfhJ1o4MmP4hmMYqgJk5X7WW4p57vhowACzRsAAoevCFfWiE6JGTvGuDYE",
    "Harry Potter Book 2": "BQACAgUAAxkBAAEfhJ9o4MngMHAnRhEtiujGwRZ0rjkQXAAC1xsAAoevCFdZMg2sI8rxUDYE",
    "Harry Potter Book 3": "BQACAgUAAxkBAAEfhKFo4Mo8quprsZu3ueRUa1DdSmCKaAAC4xsAAoevCFcLG11xRVqBvzYE",
    "Harry Potter Book 4": "BQACAgUAAxkBAAEfhKNo4MpWNUt3j5kFpHg-syCUjLzTsgAC6xsAAoevCFeziCsb2Csp6TYE",
    "Harry Potter Book 5": "BQACAgUAAxkBAAEfhJ1o4MmP4hmMYqgJk5X7WW4p57vhowACzRsAAoevCFfWiE6JGTvGuDYE",
    "Harry Potter Book 6": "BQACAgUAAxkBAAEfhJ1o4MmP4hmMYqgJk5X7WW4p57vhowACzRsAAoevCFfWiE6JGTvGuDYE",
    "Harry Potter Book 7": "BQACAgUAAxkBAAEfhJ1o4MmP4hmMYqgJk5X7WW4p57vhowACzRsAAoevCFfWiE6JGTvGuDYE",
    "project hail mary": "PASTE_YOUR_FILE_ID_FOR_PROJECT_HAIL_MARY_HERE"
}

# --- Bot Functions ---

def start(update: Update, context: CallbackContext) -> None:
    user_name = update.effective_user.first_name
    welcome_message = (
        f"Hi {user_name}! 📚🎧\n\n"
        "Welcome to the premium Audiobook library.\n\n"
        "Use /list to see all available titles.\n"
        "Use /getbook <book_name> to request a specific book."
    )
    update.message.reply_text(welcome_message)

def list_files(update: Update, context: CallbackContext) -> None:
    """Lists all available audiobooks from the catalog."""
    if not AUDIOBOOK_CATALOG:
        update.message.reply_text('Sorry, the audiobook library is empty right now. 📂')
        return
    
    # Capitalize each word for a nice, clean list
    book_titles = [title.title() for title in AUDIOBOOK_CATALOG.keys()]
    
    book_list = "\n".join([f"📖 {title}" for title in book_titles])
    message = f"Here are the available audiobooks:\n\n{book_list}"
    update.message.reply_text(message)

def get_book(update: Update, context: CallbackContext) -> None:
    """Sends an audiobook using its file_id."""
    if not context.args:
        update.message.reply_text('Please specify which book you want!\nUsage: /getbook <book_name>')
        return
    
    requested_title = " ".join(context.args).lower()
    
    if requested_title in AUDIOBOOK_CATALOG:
        file_id = AUDIOBOOK_CATALOG[requested_title]
        
        update.message.reply_text(f'Found it! Sending "{requested_title.title()}" now... This should be instant! 🚀')
        
        # Send the document using the stored file_id
        context.bot.send_document(chat_id=update.message.chat_id, document=file_id)
    else:
        update.message.reply_text(f'Sorry, I couldn\'t find a book with the title "{requested_title.title()}". 😕')

# --- Main Bot Setup ---
def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("list", list_files))
    dispatcher.add_handler(CommandHandler("getbook", get_book))

    print("ID Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()