import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
import asyncio

# Bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Sample crypto news data
CRYPTO_NEWS = [
    {
        "title": "🚀 Bitcoin Surges Past $45,000",
        "content": "Bitcoin has broken through the $45,000 resistance level, marking a 15% increase in the past 24 hours. Analysts attribute this surge to increased institutional adoption."
    },
    {
        "title": "💎 Ethereum London Upgrade Success",
        "content": "Ethereum's London hard fork has been successfully implemented, introducing EIP-1559 which changes the fee structure and could make ETH deflationary."
    },
    {
        "title": "📈 Solana Reaches New All-Time High",
        "content": "Solana (SOL) has surged 25% today, reaching a new all-time high of $150. The blockchain continues to gain traction with NFT and DeFi projects."
    },
    {
        "title": "🏦 Major Bank Announces Crypto Services",
        "content": "A leading global bank has announced it will offer cryptocurrency trading and custody services to its wealth management clients starting next month."
    },
    {
        "title": "🔄 Cardano Smart Contracts Go Live",
        "content": "Cardano has successfully launched its Alonzo hard fork, bringing smart contract functionality to the blockchain after years of development."
    },
    {
        "title": "🌍 El Salvador Adopts Bitcoin as Legal Tender",
        "content": "El Salvador has officially adopted Bitcoin as legal tender, becoming the first country in the world to do so."
    }
]

async def start_command(update: Update, context: CallbackContext):
    """Handle the /start command"""
    user = update.effective_user
    
    # Check if user has visited before
    user_id = str(user.id)
    
    # Get random crypto news
    news = random.choice(CRYPTO_NEWS)
    
    # Create welcome message with news
    welcome_message = (
        f"👋 Welcome {user.first_name}!\n\n"
        f"📰 **Today's Crypto News**\n\n"
        f"**{news['title']}**\n"
        f"{news['content']}\n\n"
        f"Stay tuned for more updates!"
    )
    
    # Create inline keyboard with button
    keyboard = [
        [InlineKeyboardButton("🤖 Check This Bot", url="https://t.me/polyssightsbot22")],
        [InlineKeyboardButton("🔄 Refresh News", callback_data="refresh_news")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send message with button
    if update.message:
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

async def refresh_news(update: Update, context: CallbackContext):
    """Handle refresh news button click"""
    query = update.callback_query
    await query.answer()
    
    # Get new random news
    news = random.choice(CRYPTO_NEWS)
    
    # Update message with new news
    refresh_message = (
        f"🔄 **News Refreshed!**\n\n"
        f"📰 **Today's Crypto News**\n\n"
        f"**{news['title']}**\n"
        f"{news['content']}\n\n"
        f"Stay tuned for more updates!"
    )
    
    # Keep the same button
    keyboard = [
        [InlineKeyboardButton("🤖 Check This Bot", url="https://t.me/polyssightsbot22")],
        [InlineKeyboardButton("🔄 Refresh News", callback_data="refresh_news")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(refresh_message, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: CallbackContext):
    """Handle the /help command"""
    help_text = (
        "🤖 **Crypto News Bot Help**\n\n"
        "/start - Get today's crypto news and bot information\n"
        "/help - Show this help message\n"
        "/news - Get a random crypto news update\n\n"
        "Click the 'Refresh News' button to get fresh news!"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def news_command(update: Update, context: CallbackContext):
    """Handle the /news command"""
    # Get random crypto news
    news = random.choice(CRYPTO_NEWS)
    
    news_message = (
        f"📰 **Crypto News Update**\n\n"
        f"**{news['title']}**\n"
        f"{news['content']}\n\n"
        f"Check back soon for more updates!"
    )
    
    await update.message.reply_text(news_message, parse_mode='Markdown')

def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("news", news_command))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(refresh_news, pattern="refresh_news"))
    
    # Start the bot
    print("🤖 Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
