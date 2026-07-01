# handlers/ziyarat_handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import sqlite3
import os

DB_PATH = os.getenv('DATABASE_PATH', 'quran_bot.db')

def get_db():
    return sqlite3.connect(DB_PATH)

async def show_ziyarat_ashura_az(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ziyarəti-Əşuranı Azərbaycanca hissələrlə göstərir"""
    query = update.callback_query
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT content_az FROM ziyarat WHERE title_az = 'Ziyarəti-Əşura'")
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        await query.edit_message_text("❌ Ziyarət tapılmadı!")
        return
    
    content_az = result[0]
    
    # Mətni hissələrə böl (hər hissə 3500 simvol)
    parts = []
    while len(content_az) > 3500:
        split_point = content_az[:3500].rfind(' ')
        if split_point == -1:
            split_point = 3500
        parts.append(content_az[:split_point])
        content_az = content_az[split_point:].strip()
    parts.append(content_az)
    
    keyboard = [[InlineKeyboardButton("🔙 Ziyarətlərə qayıt", callback_data="ziyarat_menu")]]
    
    if len(parts) == 1:
        await query.edit_message_text(
            f"📖 *Ziyarəti-Əşura (Azərbaycanca)*\n\n{parts[0]}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.edit_message_text(
            f"📖 *Ziyarəti-Əşura (Azərbaycanca) - Hissə 1/{len(parts)}*\n\n{parts[0]}",
            parse_mode="Markdown"
        )
        
        for i, part in enumerate(parts[1:], 2):
            await query.message.reply_text(
                f"📖 *Hissə {i}/{len(parts)}*\n\n{part}",
                parse_mode="Markdown"
            )
        
        await query.message.reply_text(
            "🔚 *Ziyarətin sonu*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def show_ziyarat_ashura_ar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ziyarəti-Əşuranı Ərəbcə (transkripsiya) hissələrlə göstərir"""
    query = update.callback_query
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT content_ar FROM ziyarat WHERE title_az = 'Ziyarəti-Əşura'")
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        await query.edit_message_text("❌ Ziyarət tapılmadı!")
        return
    
    content_ar = result[0]
    
    parts = []
    while len(content_ar) > 3500:
        split_point = content_ar[:3500].rfind(' ')
        if split_point == -1:
            split_point = 3500
        parts.append(content_ar[:split_point])
        content_ar = content_ar[split_point:].strip()
    parts.append(content_ar)
    
    keyboard = [[InlineKeyboardButton("🔙 Ziyarətlərə qayıt", callback_data="ziyarat_menu")]]
    
    if len(parts) == 1:
        await query.edit_message_text(
            f"📜 *Ziyarəti-Əşura (Ərəbcə)*\n\n{parts[0]}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.edit_message_text(
            f"📜 *Ziyarəti-Əşura (Ərəbcə) - Hissə 1/{len(parts)}*\n\n{parts[0]}",
            parse_mode="Markdown"
        )
        
        for i, part in enumerate(parts[1:], 2):
            await query.message.reply_text(
                f"📜 *Hissə {i}/{len(parts)}*\n\n{part}",
                parse_mode="Markdown"
            )
        
        await query.message.reply_text(
            "🔚 *Ziyarətin sonu*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )