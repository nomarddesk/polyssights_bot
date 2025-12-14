import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import random
from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable not set!")
    raise ValueError("BOT_TOKEN environment variable not set!")

# Sample crypto news
CRYPTO_NEWS = [
    {
        "title": "🚀 Bitcoin Surges Past $45,000",
        "content": "Bitcoin has broken through the $45,000 resistance level, marking a 15% increase in the past 24 hours."
    },
    {
        "title": "💎 Ethereum London Upgrade Success",
        "content": "Ethereum's London hard fork has been successfully implemented, introducing EIP-1559."
    },
    # Add more news as needed
]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    try:
        user = update.effective_user
        logger.info(f"User {user.id} ({user.first_name}) started the bot")
        
        # Get random crypto news
        news = random.choice(CRYPTO_NEWS)
        
        welcome_message = (
            f"👋 Welcome {user.first_name}!\n\n"
            f"📰 **Today's Crypto News**\n\n"
            f"**{news['title']}**\n"
            f"{news['content']}\n\n"
            f"Stay tuned for more updates!"
        )
        
        # Create inline keyboard
        keyboard = [
            [InlineKeyboardButton("🤖 Check This Bot", url="https://t.me/polyssightsbot22")],
            [InlineKeyboardButton("🔄 Refresh News", callback_data="refresh_news")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message, 
            reply_markup=reply_markup, 
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text("❌ Sorry, an error occurred. Please try again.")

async def refresh_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle refresh news button click"""
    try:
        query = update.callback_query
        await query.answer()
        
        # Get new random news
        news = random.choice(CRYPTO_NEWS)
        
        refresh_message = (
            f"🔄 **News Refreshed!**\n\n"
            f"📰 **Today's Crypto News**\n\n"
            f"**{news['title']}**\n"
            f"{news['content']}\n\n"
            f"Stay tuned for more updates!"
        )
        
        keyboard = [
            [InlineKeyboardButton("🤖 Check This Bot", url="https://t.me/polyssightsbot22")],
            [InlineKeyboardButton("🔄 Refresh News", callback_data="refresh_news")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            refresh_message, 
            reply_markup=reply_markup, 
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error in refresh_news: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    try:
        logger.info("Starting bot...")
        
        # Create Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(refresh_news, pattern="refresh_news"))
        application.add_error_handler(error_handler)
        
        # Start the bot
        logger.info("Bot is now polling for updates...")
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == '__main__':
    main()
