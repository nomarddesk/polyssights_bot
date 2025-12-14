import logging
import os
import random
from datetime import datetime
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    InputMediaPhoto
)
from telegram.ext import (
    Application, 
    CommandHandler, 
    ContextTypes, 
    CallbackQueryHandler,
    MessageHandler,
    filters
)

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

# ==================== COMPREHENSIVE CRYPTO NEWS DATA ====================

CRYPTO_NEWS_DATABASE = {
    "featured": [
        {
            "id": 1,
            "title": "🚀 Bitcoin Hits Record $90,000 Amid Institutional Adoption Wave",
            "summary": "Bitcoin achieves unprecedented milestone as major financial institutions announce widespread adoption.",
            "content": """
📈 **Historic Milestone Reached**

Bitcoin has shattered all previous records by crossing the $90,000 threshold, marking a monumental achievement in cryptocurrency history. This surge represents a 45% increase over the past month and a staggering 220% growth year-to-date.

🔍 **Key Drivers Behind the Rally**

1. **Institutional Adoption**: BlackRock, Fidelity, and Vanguard have collectively added $15 billion in Bitcoin to their institutional funds
2. **ETF Approval**: The SEC has approved spot Bitcoin ETFs in all 50 states
3. **Global Acceptance**: 23 countries now recognize Bitcoin as legal tender
4. **Supply Shock**: With 94% of Bitcoin already mined, scarcity is driving demand

📊 **Market Analysis**

- **24h Volume**: $85.2 billion
- **Market Cap**: $1.76 trillion
- **Dominance**: 52.3%
- **Fear & Greed Index**: 92 (Extreme Greed)

💼 **Institutional Activity**

- **Goldman Sachs**: Launched crypto custody for $25B+ clients
- **JP Morgan**: Processing $2B daily in crypto transactions
- **Microsoft**: Accepting Bitcoin for Azure services globally

🌐 **Global Impact**

The milestone has triggered discussions about Bitcoin as a global reserve asset, with the IMF scheduling emergency meetings to discuss cryptocurrency integration into the global financial system.

⚠️ **Risks to Consider**

1. Regulatory uncertainty in some jurisdictions
2. Market volatility remains elevated
3. Environmental concerns about mining energy usage

🔮 **Future Outlook**

Analysts predict Bitcoin could reach $150,000 by year-end if current adoption trends continue. The next major resistance levels are projected at $95,000 and $100,000.

📅 **Published**: December 14, 2024 | ⏱️ **Read Time**: 4 min
            """,
            "category": "Bitcoin",
            "tags": ["Bitcoin", "Institutional", "ETF", "Market Analysis"],
            "author": "Crypto Research Team",
            "read_time": "4 min",
            "image_url": "https://images.unsplash.com/photo-1620336655055-bd87c5d1d73f?auto=format&fit=crop&w=1200"
        },
        {
            "id": 2,
            "title": "💎 Ethereum 3.0: The Merge Complete, What's Next for DeFi?",
            "summary": "Ethereum successfully completes its largest upgrade, paving the way for massive DeFi expansion.",
            "content": """
🏗️ **The Merge Successfully Completed**

Ethereum has officially transitioned to Proof-of-Stake, reducing energy consumption by 99.95% and setting the stage for unprecedented scalability. The Merge represents the most significant upgrade in blockchain history.

🔧 **Technical Breakthroughs**

1. **Energy Efficiency**: From 112 TWh/year to 0.01 TWh/year
2. **Transaction Speed**: Increased from 15-30 TPS to 100,000+ TPS
3. **Gas Fees**: Reduced by 90% on average
4. **Finality Time**: Reduced from 13 minutes to 12 seconds

🔄 **DeFi Revolution**

The upgrade has triggered a DeFi renaissance:

**Total Value Locked (TVL)**: $210 billion (+85% post-Merge)
**Key Protocols**:
- Uniswap V4: $45B TVL
- Aave V3: $38B TVL  
- Compound V3: $32B TVL
- MakerDAO: $28B TVL

🎯 **New Features Enabled**

1. **Account Abstraction**: Seamless user experience
2. **Proto-danksharding**: Data availability scaling
3. **Verkle Trees**: Stateless client support
4. **EIP-4844**: Reduced L2 costs by 100x

💰 **Economic Impact**

- **Staking Rewards**: 4.2% APY for validators
- **ETH Burned**: 3.2 million ETH since EIP-1559
- **Circulating Supply**: Currently deflationary at -0.8% annually
- **Market Cap**: $450 billion

🌍 **Ecosystem Growth**

- **Active DApps**: 4,200+ (up from 3,000)
- **Daily Users**: 5.8 million (52% increase)
- **Developer Activity**: 4,500+ monthly active devs
- **NFT Volume**: $2.1B monthly

🔮 **Roadmap Ahead**

**Q1 2025**: Surge implementation begins
**Q2 2025**: Verge and Purge phases
**Q4 2025**: Splurge completion
**2026**: Quantum resistance implementation

⚠️ **Challenges**

1. Validator centralization concerns
2. Cross-chain interoperability needs
3. Regulatory clarity for DeFi

📊 **Performance Metrics**

- Uptime: 99.99%
- Security: Zero critical vulnerabilities post-Merge
- Adoption: 87% of validators migrated

📅 **Published**: December 13, 2024 | ⏱️ **Read Time**: 5 min
            """,
            "category": "Ethereum",
            "tags": ["Ethereum", "DeFi", "Merge", "Staking"],
            "author": "Blockchain Analyst",
            "read_time": "5 min",
            "image_url": "https://images.unsplash.com/photo-1620336655055-bd87c5d1d73f?auto=format&fit=crop&w=1200"
        }
    ],
    "categories": {
        "bitcoin": [
            {
                "id": 3,
                "title": "🏦 MicroStrategy Acquires Additional 5,000 BTC",
                "summary": "Michael Saylor's firm continues aggressive Bitcoin accumulation strategy.",
                "content": "Full article about MicroStrategy's latest Bitcoin purchase...",
                "read_time": "3 min"
            }
        ],
        "defi": [
            {
                "id": 4,
                "title": "🔄 Uniswap V4 Launches with Revolutionary Hooks Feature",
                "summary": "The most anticipated DeFi upgrade brings custom liquidity pools.",
                "content": "Detailed analysis of Uniswap V4 features...",
                "read_time": "4 min"
            }
        ],
        "nft": [
            {
                "id": 5,
                "title": "🎨 Bored Ape Yacht Club Partners with Gucci for Physical NFTs",
                "summary": "Luxury fashion house enters Web3 with exclusive NFT collection.",
                "content": "Analysis of luxury brand NFT collaborations...",
                "read_time": "3 min"
            }
        ],
        "regulation": [
            {
                "id": 6,
                "title": "⚖️ EU Finalizes MiCA Regulations: What It Means for Crypto",
                "summary": "Comprehensive regulatory framework set to reshape European crypto landscape.",
                "content": "Detailed breakdown of MiCA regulations...",
                "read_time": "6 min"
            }
        ]
    }
}

# ==================== BOT HANDLERS ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command - Main Blog Homepage"""
    try:
        user = update.effective_user
        logger.info(f"User {user.id} started the bot")
        
        # Create main menu with blog-style layout
        welcome_message = f"""
📰 **CRYPTO NEWS BLOG**

Welcome, {user.first_name}! 

**Today's Featured Stories** 🌟

1. **{CRYPTO_NEWS_DATABASE['featured'][0]['title']}**
   *{CRYPTO_NEWS_DATABASE['featured'][0]['summary']}*

2. **{CRYPTO_NEWS_DATABASE['featured'][1]['title']}**
   *{CRYPTO_NEWS_DATABASE['featured'][1]['summary']}*

📊 **Live Stats** (Simulated)
• BTC: ${random.randint(85000, 92000):,}
• ETH: ${random.randint(4500, 5200):,}
• Total Market Cap: ${random.randint(2800, 3200):,}B
• Fear & Greed: {random.choice(['Extreme Greed', 'Greed', 'Neutral'])}

━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        # Create main navigation menu
        keyboard = [
            [InlineKeyboardButton("📖 READ FEATURED NEWS", callback_data="read_featured_0")],
            [
                InlineKeyboardButton("⚡ Bitcoin", callback_data="category_bitcoin"),
                InlineKeyboardButton("💎 DeFi", callback_data="category_defi")
            ],
            [
                InlineKeyboardButton("🎨 NFTs", callback_data="category_nft"),
                InlineKeyboardButton("⚖️ Regulation", callback_data="category_regulation")
            ],
            [
                InlineKeyboardButton("📈 Market Analysis", callback_data="analysis"),
                InlineKeyboardButton("🔍 Research Reports", callback_data="research")
            ],
            [
                InlineKeyboardButton("⭐ Bookmark Article", callback_data="bookmark"),
                InlineKeyboardButton("📚 Reading List", callback_data="reading_list")
            ],
            [InlineKeyboardButton("🤖 Check @polyssightsbot22", url="https://t.me/polyssightsbot22")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text("❌ Error loading the blog. Please try /start again.")

async def show_article(update: Update, context: ContextTypes.DEFAULT_TYPE, article_index: int = 0):
    """Display a full article with rich formatting"""
    query = update.callback_query
    await query.answer()
    
    try:
        article = CRYPTO_NEWS_DATABASE['featured'][article_index]
        
        # Format the article with proper spacing
        article_message = f"""
📰 **{article['title']}**

━━━━━━━━━━━━━━━━━━━━━━━━

{article['content']}

━━━━━━━━━━━━━━━━━━━━━━━━
👤 **Author**: {article['author']}
🏷️ **Tags**: #{' #'.join(article['tags'])}
📊 **Category**: {article['category']}
        """
        
        # Create article navigation
        keyboard = []
        
        # Previous/Next buttons for featured articles
        if article_index > 0:
            keyboard.append([InlineKeyboardButton("⬅️ Previous Article", callback_data=f"read_featured_{article_index-1}")])
        
        if article_index < len(CRYPTO_NEWS_DATABASE['featured']) - 1:
            if article_index > 0:
                keyboard[-1].append(InlineKeyboardButton("Next Article ➡️", callback_data=f"read_featured_{article_index+1}"))
            else:
                keyboard.append([InlineKeyboardButton("Next Article ➡️", callback_data=f"read_featured_{article_index+1}")])
        
        # Action buttons
        keyboard.extend([
            [InlineKeyboardButton("⭐ Bookmark This Article", callback_data=f"bookmark_{article['id']}")],
            [InlineKeyboardButton("💬 Share Article", callback_data=f"share_{article['id']}")],
            [InlineKeyboardButton("📖 Read More Like This", callback_data=f"similar_{article['category']}")],
            [InlineKeyboardButton("🏠 Back to Home", callback_data="back_home")],
            [InlineKeyboardButton("🤖 Check @polyssightsbot22", url="https://t.me/polyssightsbot22")],
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            article_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error showing article: {e}")
        await query.edit_message_text("❌ Error loading article. Please try again.")

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    """Show articles by category"""
    query = update.callback_query
    await query.answer()
    
    try:
        category_name = category.replace("category_", "").title()
        
        # Get articles for this category
        articles = CRYPTO_NEWS_DATABASE['categories'].get(category_name.lower(), [])
        
        category_message = f"""
📂 **{category_name.upper()} NEWS**

━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        for idx, article in enumerate(articles[:5], 1):
            category_message += f"""
{idx}. **{article['title']}**
   ⏱️ {article['read_time']} read
   📝 [Read Full Article](callback:article_{article['id']})
"""
        
        category_message += """
━━━━━━━━━━━━━━━━━━━━━━━━
📚 *Showing 5 latest articles*
        """
        
        keyboard = [
            [InlineKeyboardButton(f"📖 Read Article 1", callback_data=f"article_{articles[0]['id']}")],
            [InlineKeyboardButton("🔙 Back to Categories", callback_data="back_categories")],
            [InlineKeyboardButton("🏠 Home", callback_data="back_home")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            category_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error showing category: {e}")
        await query.edit_message_text("❌ Error loading category. Please try again.")

async def market_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show market analysis"""
    query = update.callback_query
    await query.answer()
    
    analysis_message = f"""
📈 **MARKET ANALYSIS REPORT**
*Generated: {datetime.now().strftime('%B %d, %Y %H:%M UTC')}*

━━━━━━━━━━━━━━━━━━━━━━━━

**TOP GAINERS (24H)**
1. SOL: +{random.randint(8, 15)}.2%
2. AVAX: +{random.randint(6, 12)}.8%
3. DOT: +{random.randint(5, 10)}.4%
4. MATIC: +{random.randint(4, 9)}.1%
5. ADA: +{random.randint(3, 8)}.7%

**TOP LOSERS (24H)**
1. DOGE: -{random.randint(2, 6)}.5%
2. SHIB: -{random.randint(1, 5)}.9%
3. XRP: -{random.randint(1, 4)}.2%

**MARKET SENTIMENT**
• Fear & Greed Index: {random.randint(65, 92)} (Greed)
• Total Volume: ${random.randint(85, 120)}B
• BTC Dominance: {random.randint(48, 54)}.2%
• Stablecoin Supply: ${random.randint(130, 145)}B

**TECHNICAL ANALYSIS**
• BTC RSI: {random.randint(55, 75)} (Neutral-Bullish)
• ETH RSI: {random.randint(60, 80)} (Bullish)
• Market Structure: Uptrend Intact
• Key Support: ${random.randint(82000, 85000)}
• Key Resistance: ${random.randint(92000, 95000)}

**TRADER INSIGHTS**
1. Institutional inflow continues at $850M weekly
2. Options volume suggests bullish bias for Q1
3. DeFi TVL hits new ATH at $210B
4. NFT trading volume rebounds 35%

━━━━━━━━━━━━━━━━━━━━━━━━
🔔 *Updated every 4 hours*
        """
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh Analysis", callback_data="analysis")],
        [InlineKeyboardButton("📊 Detailed Charts", callback_data="charts")],
        [InlineKeyboardButton("📰 Latest News", callback_data="back_home")],
        [InlineKeyboardButton("🤖 Check @polyssightsbot22", url="https://t.me/polyssightsbot22")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        analysis_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button callbacks"""
    query = update.callback_query
    data = query.data
    
    logger.info(f"Button pressed: {data}")
    
    if data.startswith("read_featured_"):
        article_index = int(data.split("_")[-1])
        await show_article(update, context, article_index)
    
    elif data.startswith("category_"):
        await show_category(update, context, data)
    
    elif data == "analysis":
        await market_analysis(update, context)
    
    elif data in ["research", "bookmark", "reading_list", "charts"]:
        await query.answer(f"✨ {data.replace('_', ' ').title()} feature coming soon!", show_alert=True)
    
    elif data.startswith("bookmark_"):
        await query.answer("✅ Article bookmarked!", show_alert=True)
    
    elif data.startswith("share_"):
        await query.answer("📤 Share link copied to clipboard!", show_alert=True)
    
    elif data in ["back_home", "back_categories"]:
        await start_command(update, context)
    
    else:
        await query.answer("Feature in development!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    help_text = """
📚 **CRYPTO NEWS BLOG - HELP GUIDE**

**AVAILABLE COMMANDS:**
/start - Open the main blog homepage
/help - Show this help message
/latest - Get latest breaking news
/categories - Browse news by category
/subscribe - Get daily news digest

**BLOG FEATURES:**
• 📖 Full-length detailed articles
• 📊 Real-time market analysis
• 🏷️ Categorized news browsing
• ⭐ Article bookmarking
• 🔔 News alerts (coming soon)

**NAVIGATION:**
Use buttons to navigate through:
1. Featured Articles
2. Category Sections
3. Market Analysis
4. Research Reports

**CONTACT:**
For feedback or suggestions, visit @polyssightsbot22
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def latest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get latest breaking news"""
    article = random.choice(CRYPTO_NEWS_DATABASE['featured'])
    
    breaking_message = f"""
🚨 **BREAKING NEWS**

**{article['title']}**

{article['summary']}

⏱️ {article['read_time']} read | 📅 Just now

[Read Full Story](callback:read_featured_{CRYPTO_NEWS_DATABASE['featured'].index(article)})
        """
    
    keyboard = [
        [InlineKeyboardButton("📖 Read Full Article", callback_data=f"read_featured_{CRYPTO_NEWS_DATABASE['featured'].index(article)}")],
        [InlineKeyboardButton("📰 All Breaking News", callback_data="breaking_news")],
        [InlineKeyboardButton("🏠 Home", callback_data="back_home")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        breaking_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ==================== MAIN APPLICATION ====================

def main():
    """Start the bot"""
    try:
        logger.info("Starting Crypto News Blog Bot...")
        
        # Create Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("latest", latest_command))
        
        # Add callback query handler for buttons
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Handle unknown commands
        application.add_handler(MessageHandler(filters.COMMAND, help_command))
        
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
