import logging
import os
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

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

# Featured bot link
POLYSSIGHTS_BOT = "@polyssightsbot"

# Simple news database
NEWS_ITEMS = [
    "🚀 **Bitcoin Breaks $90,000 Barrier**\nBitcoin has surged past the $90,000 mark for the first time, driven by institutional adoption and ETF approvals.",
    "💎 **Ethereum 3.0 Upgrade Complete**\nThe Ethereum network has successfully completed its largest upgrade, reducing energy consumption by 99.95%.",
    "🏦 **Major Bank Launches Crypto Division**\nA leading global bank has announced a dedicated cryptocurrency trading desk for institutional clients.",
    "🌍 **Digital Dollar Pilot Launches**\nThe US Federal Reserve has begun testing a central bank digital currency with select financial institutions.",
    "📊 **DeFi TVL Hits $250 Billion**\nTotal Value Locked in decentralized finance protocols has reached a new all-time high.",
    "🎨 **NFT Market Sees 300% Growth**\nThe NFT market has experienced explosive growth with luxury brands entering the space.",
    "⚖️ **EU Finalizes Crypto Regulations**\nThe European Union has approved comprehensive cryptocurrency regulations set to take effect next year.",
    "🔒 **Crypto Security Standards Updated**\nNew global security standards for cryptocurrency exchanges have been announced."
]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command - Focus on promoting @polyssightsbot"""
    try:
        user = update.effective_user
        logger.info(f"User {user.id} started the bot")
        
        # Get random news
        news = random.choice(NEWS_ITEMS)
        
        # Create message with prominent bot promotion
        welcome_message = f"""
🌟 **WELCOME TO CRYPTO NEWS UPDATES** 🌟

👋 Hello {user.first_name}!

📰 **Today's Crypto Headline:**
{news}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 **MAIN FEATURE BOT:** 🔥

**👉 @polyssightsbot 👈**

📊 **Why Follow @polyssightsbot?**
• 📈 Real-time market insights
• 🔔 Instant price alerts
• 📊 Technical analysis
• 🚀 Trading signals
• 📰 Breaking news updates

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 **This Bot's Features:**
✅ Daily crypto news summaries
✅ Market trend analysis
✅ Quick updates on major events
✅ Easy navigation

📌 *Click the button below to visit our main bot for comprehensive crypto analysis!*
        """
        
        # Create keyboard with prominent button for @polyssightsbot
        keyboard = [
            [InlineKeyboardButton("🔥 VISIT MAIN BOT 🔥", url=f"https://t.me/polyssightsbot")],
            [InlineKeyboardButton("📰 Get Another News", callback_data="new_news")],
            [InlineKeyboardButton("📊 Market Summary", callback_data="market_summary")],
            [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text("❌ Error loading news. Please try /start again.")

async def new_news_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle new news button click"""
    query = update.callback_query
    await query.answer()
    
    try:
        # Get new random news
        news = random.choice(NEWS_ITEMS)
        
        # Update message with new news
        news_message = f"""
🔄 **Fresh News Update**

📰 **Latest Headline:**
{news}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 **Don't forget to check our main bot:**
👉 **@{POLYSSIGHTS_BOT.replace('@', '')}** 👈

*For comprehensive crypto analysis, trading signals, and real-time alerts!*
        """
        
        # Keep the same keyboard
        keyboard = [
            [InlineKeyboardButton("🔥 VISIT MAIN BOT 🔥", url=f"https://t.me/{POLYSSIGHTS_BOT.replace('@', '')}")],
            [InlineKeyboardButton("📰 Get Another News", callback_data="new_news")],
            [InlineKeyboardButton("📊 Market Summary", callback_data="market_summary")],
            [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            news_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error in new_news_handler: {e}")

async def market_summary_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle market summary button click"""
    query = update.callback_query
    await query.answer()
    
    # Generate simulated market data
    btc_price = random.randint(85000, 95000)
    eth_price = random.randint(4500, 5200)
    market_cap = random.randint(2800, 3200)
    
    summary_message = f"""
📊 **CRYPTO MARKET SUMMARY**
*As of {datetime.now().strftime('%H:%M UTC')}*

━━━━━━━━━━━━━━━━━━━━━━━━

💰 **Top Assets:**
• **Bitcoin (BTC):** ${btc_price:,} ({random.choice(['+', '-'])}{random.randint(1, 5)}.{random.randint(1, 9)}%)
• **Ethereum (ETH):** ${eth_price:,} ({random.choice(['+', '-'])}{random.randint(1, 4)}.{random.randint(1, 9)}%)
• **Total Market Cap:** ${market_cap}B

📈 **Market Sentiment:**
• Fear & Greed Index: {random.randint(55, 85)} ({random.choice(['Greed', 'Extreme Greed', 'Neutral'])})
• 24h Volume: ${random.randint(85, 120)}B
• BTC Dominance: {random.randint(48, 54)}.2%

🔔 **Key Events Today:**
1. {random.choice(['Fed meeting minutes', 'CPI data release', 'Major exchange listing'])}
2. {random.choice(['Institutional inflow report', 'Regulatory announcement', 'Network upgrade'])}

━━━━━━━━━━━━━━━━━━━━━━━━

🔥 **For detailed analysis and alerts, visit:**
👉 **@{POLYSSIGHTS_BOT.replace('@', '')}** 👈
        """
    
    keyboard = [
        [InlineKeyboardButton("🔥 VISIT MAIN BOT 🔥", url=f"https://t.me/{POLYSSIGHTS_BOT.replace('@', '')}")],
        [InlineKeyboardButton("📰 Get News", callback_data="new_news")],
        [InlineKeyboardButton("🔄 Refresh Summary", callback_data="market_summary")],
        [InlineKeyboardButton("🏠 Back to Start", callback_data="back_home")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        summary_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle about button click"""
    query = update.callback_query
    await query.answer()
    
    about_message = f"""
ℹ️ **ABOUT THIS BOT**

━━━━━━━━━━━━━━━━━━━━━━━━

📱 **Purpose:**
This bot provides quick crypto news updates and market summaries. It serves as a companion to our main analytics bot.

🌟 **Main Bot:**
**👉 {POLYSSIGHTS_BOT} 👈**

**Features of {POLYSSIGHTS_BOT}:**
✅ Real-time price tracking
✅ Technical analysis charts
✅ Trading signals & alerts
✅ Portfolio management
✅ Market sentiment analysis
✅ News aggregation

📊 **This Bot's Features:**
• Daily news headlines
• Market summaries
• Quick updates
• Easy navigation to main bot

🔗 **Connect With Us:**
• Main Bot: {POLYSSIGHTS_BOT}
• Updates Channel: Coming soon
• Support: Contact via main bot

━━━━━━━━━━━━━━━━━━━━━━━━

💡 *For comprehensive crypto analysis and trading tools, always check our main bot!*
        """
    
    keyboard = [
        [InlineKeyboardButton("🔥 VISIT MAIN BOT 🔥", url=f"https://t.me/{POLYSSIGHTS_BOT.replace('@', '')}")],
        [InlineKeyboardButton("📰 Get News", callback_data="new_news")],
        [InlineKeyboardButton("📊 Market Summary", callback_data="market_summary")],
        [InlineKeyboardButton("🏠 Back to Start", callback_data="back_home")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        about_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button callbacks"""
    query = update.callback_query
    data = query.data
    
    logger.info(f"Button pressed: {data}")
    
    if data == "new_news":
        await new_news_handler(update, context)
    
    elif data == "market_summary":
        await market_summary_handler(update, context)
    
    elif data == "about":
        await about_handler(update, context)
    
    elif data == "back_home":
        # Simulate start command
        user = query.from_user
        context.user_data['user'] = user
        await start_command(update, context)
    
    else:
        await query.answer("Feature coming soon!", show_alert=True)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    help_text = f"""
🤖 **CRYPTO NEWS BOT HELP**

━━━━━━━━━━━━━━━━━━━━━━━━

**COMMANDS:**
/start - Get crypto news and visit main bot
/help - Show this help message
/news - Get a random crypto news update
/market - Get market summary

**MAIN BOT:**
👉 **{POLYSSIGHTS_BOT}** 👈

**Features of main bot:**
• 📈 Real-time price tracking
• 🔔 Custom alerts
• 📊 Technical analysis
• 🚀 Trading signals
• 📰 News aggregation

**HOW TO USE:**
1. Click /start to begin
2. Use buttons to navigate
3. Click the main button to visit {POLYSSIGHTS_BOT}
4. Get news updates anytime

━━━━━━━━━━━━━━━━━━━━━━━━

💡 *Always check {POLYSSIGHTS_BOT} for comprehensive analysis!*
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /news command"""
    news = random.choice(NEWS_ITEMS)
    
    news_message = f"""
📰 **CRYPTO NEWS UPDATE**

{news}

━━━━━━━━━━━━━━━━━━━━━━━━

🔥 **For more detailed analysis, visit:**
👉 **{POLYSSIGHTS_BOT}** 👈
"""
    
    keyboard = [
        [InlineKeyboardButton("🔥 VISIT MAIN BOT 🔥", url=f"https://t.me/{POLYSSIGHTS_BOT.replace('@', '')}")],
        [InlineKeyboardButton("📰 Another News", callback_data="new_news")],
        [InlineKeyboardButton("📊 Market Summary", callback_data="market_summary")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        news_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def market_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /market command"""
    # Simulate start of market summary
    query = update.callback_query
    if query:
        await market_summary_handler(update, context)
    else:
        # Create a fake query object for command
        class FakeQuery:
            def __init__(self):
                self.data = "market_summary"
                self.from_user = update.effective_user
            
            async def answer(self, *args, **kwargs):
                pass
        
        fake_query = FakeQuery()
        update.callback_query = fake_query
        await market_summary_handler(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any text message"""
    user_message = update.message.text.lower()
    
    if any(word in user_message for word in ['polyssights', 'main bot', 'analytics']):
        response = f"""
🔍 **Looking for our main bot?**

👉 **{POLYSSIGHTS_BOT}** 👈

Click the button below to visit it now!
"""
        
        keyboard = [[InlineKeyboardButton("🔥 VISIT MAIN BOT 🔥", url=f"https://t.me/{POLYSSIGHTS_BOT.replace('@', '')}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif any(word in user_message for word in ['news', 'update', 'headline']):
        await news_command(update, context)
    
    elif any(word in user_message for word in ['price', 'market', 'summary']):
        await market_command(update, context)
    
    else:
        response = f"""
🤔 Not sure what you're looking for?

Try these commands:
/start - Main menu with {POLYSSIGHTS_BOT} link
/news - Latest crypto news
/market - Market summary
/help - Help guide

Or just type what you're looking for!
"""
        await update.message.reply_text(response, parse_mode='Markdown')

def main():
    """Start the bot"""
    try:
        logger.info("Starting Crypto News Bot with @polyssightsbot promotion...")
        
        # Create Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("news", news_command))
        application.add_handler(CommandHandler("market", market_command))
        
        # Add callback query handler for buttons
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Handle text messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Start the bot
        logger.info("Bot is now polling for updates...")
        logger.info(f"Promoting main bot: {POLYSSIGHTS_BOT}")
        
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == '__main__':
    main()
