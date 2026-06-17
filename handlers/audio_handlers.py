# handlers/audio_handlers.py
import os
import sqlite3
from io import BytesIO
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# ⚠️ Burada get_db funksiyasını təkrar yazırıq (dövrü import olmasın deyə)
DB_PATH = os.getenv('DATABASE_PATH', 'quran_bot.db')

def get_db():
    return sqlite3.connect(DB_PATH)

# Audio cache
_surah_audio_cache = {}

def get_surah_audio_from_disk(surah_no: int, mp3_folder: str = "Quran_mp3"):
    """Surə audio faylını diskdən oxuyur"""
    if surah_no in _surah_audio_cache:
        audio_data = _surah_audio_cache[surah_no]
        audio_data.seek(0)
        return audio_data
    
    mp3_path = os.path.join(mp3_folder, f"{surah_no:03d}.mp3")
    
    if not os.path.exists(mp3_path):
        print(f"⚠️ Audio tapılmadı: {mp3_path}")
        return None
    
    with open(mp3_path, 'rb') as f:
        audio_data = BytesIO(f.read())
        audio_data.name = f"{surah_no:03d}.mp3"
        _surah_audio_cache[surah_no] = audio_data
        return audio_data

async def play_surah_audio(update: Update, context: ContextTypes.DEFAULT_TYPE, surah_no: int):
    """Surə audio faylını göndərir"""
    query = update.callback_query
    
    # Dərhal cavab
    await query.message.reply_text(
        "⏳ *Audio hazırlanır...*\n📤 Bir neçə saniyə gözləyin.",
        parse_mode="Markdown"
    )
    
    # Audio faylını al
    audio_data = get_surah_audio_from_disk(surah_no)
    
    if not audio_data:
        await query.message.reply_text(
            f"❌ *Audio tapılmadı!*\n\n⚠️ {surah_no}. surə tapılmadı.",
            parse_mode="Markdown"
        )
        return
    
    # Surə adını al
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name_az FROM surahs WHERE order_no = ?", (surah_no,))
    result = cursor.fetchone()
    conn.close()
    
    surah_name = result[0] if result else f"{surah_no}"
    file_size_mb = audio_data.getbuffer().nbytes / (1024 * 1024)
    
    # Audio göndər
    await context.bot.send_audio(
        chat_id=query.message.chat_id,
        audio=InputFile(audio_data, filename=f"{surah_no:03d}_{surah_name}.mp3"),
        title=f"{surah_no}. {surah_name} surəsi",
        performer="Quran",
        caption=(
            f"🎵 *{surah_no}. {surah_name} surəsi*\n"
            f"📏 {file_size_mb:.1f} MB\n\n"
            f"▶️ *Dinlə:* ▶️ düyməsinə kliklə\n"
            f"⬇️ *Yüklə:* ⬇️ düyməsinə kliklə"
        ),
        parse_mode="Markdown",
        write_timeout=300,
        read_timeout=300,
        connect_timeout=120
    )

async def show_audio_surahs(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0):
    """Audio surələrin siyahısını göstərir"""
    query = update.callback_query
    
    conn = get_db()
    cursor = conn.cursor()
    
    per_page = 10
    offset = page * per_page
    
    cursor.execute("SELECT order_no, name_az, verses_count FROM surahs ORDER BY order_no LIMIT ? OFFSET ?", (per_page, offset))
    surah_list = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM surahs")
    total = cursor.fetchone()[0]
    conn.close()
    
    total_pages = (total + per_page - 1) // per_page
    
    keyboard = []
    for order, name, verses in surah_list:
        keyboard.append([InlineKeyboardButton(
            f"🎵 {order}. {name} ({verses} ayə)",
            callback_data=f"play_audio_{order}"
        )])
    
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("◀️ Əvvəlki", callback_data=f"audio_surahs_{page-1}"))
    if page + 1 < total_pages:
        nav_row.append(InlineKeyboardButton("Sonrakı ▶️", callback_data=f"audio_surahs_{page+1}"))
    if nav_row:
        keyboard.append(nav_row)
    
    keyboard.append([InlineKeyboardButton("🏠 Əsas menyu", callback_data="main_menu")])
    
    msg = f"🎵 *Qurani-Kerim dinlə* ({page+1}/{total_pages})\n\n👇 Surə adına klikləyin:"
    
    await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))