import os
import sqlite3
import asyncio
import traceback
from io import BytesIO
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
# Audio handler-ları import et
from handlers.audio_handlers import show_audio_surahs, play_surah_audio
from handlers.ziyarat_handlers import show_ziyarat_ashura_ar, show_ziyarat_ashura_az

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DB_PATH = os.getenv('DATABASE_PATH', 'quran_bot.db')
GROUP_LINK = os.getenv('GROUP_LINK', 'https://t.me/quran_bot_group')

def get_db():
    return sqlite3.connect(DB_PATH)

user_data = {}

# ==================== GİZLİ QAPI (GOCHAT) ====================

# İstifadəçi klik sayını saxlamaq üçün
user_gochat_clicks = {}

# 🔥 Öz Telegram ID-nizi yazın (isteğe bağlı - yalnız sizin üçün)
ALLOWED_USER_ID = 123456789  # Öz ID-nizi yazın! [@userinfobot](https://t.me/userinfobot)

async def gochat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/gochat komandası - gizli qapı"""
    user_id = update.effective_user.id
    
    # 🔥 Yalnız sizin üçün aktiv etmək istəyirsinizsə, aşağıdakı şərhi silin
    # if user_id != ALLOWED_USER_ID:
    #     await update.message.reply_text("❌ Bilinməyən əmr!")
    #     return
    
    # Klik sayını sıfırla
    user_gochat_clicks[user_id] = 0
    
    keyboard = [
        [InlineKeyboardButton("🔄 Yenidən cəhd et", callback_data="gochat_click")]
    ]
    
    await update.message.reply_text(
        "🔍 *Axtarışınız uğurla nəticələnmədi.*\n"
        "Zəhmət olmasa *'Yenidən cəhd et'* düyməsinə 3 dəfə klikləyin.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def gochat_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yenidən cəhd et düyməsinə klikləndikdə"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    # Klik sayını artır
    if user_id not in user_gochat_clicks:
        user_gochat_clicks[user_id] = 0
    user_gochat_clicks[user_id] += 1
    
    click_count = user_gochat_clicks[user_id]
    
    if click_count >= 3:
        # 🔥 3-cü klikdə gizli linki göstər
        await query.message.edit_text(
            "🔓 *Gizli qapı açıldı!*\n\n"
            "📍 https://mychatapp-production-c2ce.up.railway.app/",  # 🔥 Linki dəyişin!
            parse_mode="Markdown"
        )
        # Klik sayını sıfırla
        user_gochat_clicks[user_id] = 0
    else:
        # Hələ 3 klik olmayıb
        remaining = 3 - click_count
        await query.answer(f"⏳ {remaining} klik qaldı!")
        
        # Mesajı yeniləmə
        keyboard = [
            [InlineKeyboardButton(f"🔄 Yenidən cəhd et ({remaining} klik qaldı)", callback_data="gochat_click")]
        ]
        await query.edit_message_text(
            "🔍 *Axtarışınız uğurla nəticələnmədi.*\n"
            f"Zəhmət olmasa *'Yenidən cəhd et'* düyməsinə {remaining} dəfə klikləyin.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ==================== BAŞLANGIÇ VƏ MENYULAR ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 Qurani-Kerim Oxu", callback_data="surahs_0")],
        [InlineKeyboardButton("🎵 Qurani-Kerim Dinlə", callback_data="audio_surahs_0")],
        [InlineKeyboardButton("🌙 Təsadüfi Ayə", callback_data="random")],
        [InlineKeyboardButton("🔍 Axtarış", callback_data="search")],
        [InlineKeyboardButton("📜 Ziyarətlər", callback_data="ziyarat_menu")],
        [InlineKeyboardButton("🏴 Heyhat_minnez_zillet", url=GROUP_LINK)],
        [InlineKeyboardButton("📜 Hədislər", callback_data="hadiths")],
        [InlineKeyboardButton("📚 Nəhсül-Bəlağə", callback_data="nahjul")],
        [InlineKeyboardButton("📘 Biharul-Ənvar", callback_data="bihar")]
    ]
    
    welcome_text = (
        "🌙 *Salam, Quran Bot-a xoş gəldiniz!*\n\n"
        "📖 Bu bot sizə Quran oxumaq, dinləmək və öyrənmək imkanı verir.\n\n"
        "👇 *Aşağıdakı menyudan seçim edin:*"
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 Qurani-Kerim Oxu", callback_data="surahs_0")],
        [InlineKeyboardButton("🎵 Qurani-Kerim Dinlə", callback_data="audio_surahs_0")],
        [InlineKeyboardButton("🌙 Təsadüfi Ayə", callback_data="random")],
        [InlineKeyboardButton("🔍 Axtarış", callback_data="search")],
        [InlineKeyboardButton("📜 Ziyarətlər", callback_data="ziyarat_menu")],
        [InlineKeyboardButton("🏴 Heyhat_minnez_zillet", url=GROUP_LINK)],
        [InlineKeyboardButton("📜 Hədislər", callback_data="hadiths")],
        [InlineKeyboardButton("📚 Nəhсül-Bəlağə", callback_data="nahjul")],
        [InlineKeyboardButton("📘 Biharul-Ənvar", callback_data="bihar")]
    ]
    
    await update.callback_query.edit_message_text(
        "🌙 *Əsas menyu*\n\n👇 *Seçim edin:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ==================== HAZIRLIQ BÖLMƏLƏRİ ====================

async def hadiths_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="main_menu")]]
    await update.callback_query.edit_message_text(
        "📜 *Hədislər*\n\n⚠️ Bu bölmə hazırlanır.\nTezliklə əlavə olunacaq.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def nahjul_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="main_menu")]]
    await update.callback_query.edit_message_text(
        "📚 *Nəhсül-Bəlağə*\n\n⚠️ Bu bölmə hazırlanır.\nTezliklə əlavə olunacaq.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def bihar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="main_menu")]]
    await update.callback_query.edit_message_text(
        "📘 *Biharul-Ənvar*\n\n⚠️ Bu bölmə hazırlanır.\nTezliklə əlavə olunacaq.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ==================== AXTARIŞ ====================

async def search_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="main_menu")]]
    msg = (
        "🔍 *Axtarış*\n\n"
        "📝 Axtarmaq istədiyiniz kəliməni yazın:\n"
        "`/search [kəlimə]`\n\n"
        "Məsələn: `/search rəhmət`"
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            msg,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            msg,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❗ *Düzgün istifadə:*\n`/search [kəlimə]`\n\nMəsələn: `/search Allah`",
            parse_mode="Markdown"
        )
        return
    
    keyword = ' '.join(context.args)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT s.name_az, v.verse_no, v.text_az 
                      FROM verses v 
                      JOIN surahs s ON v.surah_id = s.id 
                      WHERE v.text_az LIKE ? 
                      LIMIT 15''', (f'%{keyword}%',))
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        await update.message.reply_text(f"❌ *'{keyword}'* tapılmadı.", parse_mode="Markdown")
        return
    
    response = f"🔍 *'{keyword}' - Nəticələr:*\n\n"
    for surah_name, verse_no, text_az in results:
        short_text = text_az[:100] + "..." if len(text_az) > 100 else text_az
        response += f"📖 *{surah_name} {verse_no}*: {short_text}\n\n"
    
    if len(response) > 4000:
        response = response[:4000] + "\n\n... (daha çox nəticə var)"
    
    keyboard = [[InlineKeyboardButton("🏠 Əsas menyu", callback_data="main_menu")]]
    await update.message.reply_text(response, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== SURƏLƏR (MƏTN) ====================

async def show_surahs(update: Update, context: ContextTypes.DEFAULT_TYPE, page=0):
    """Surələrin siyahısını göstərir (10-luq hissələrlə)"""
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['surah_page'] = page
    
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
        keyboard.append([InlineKeyboardButton(f"{order}. {name} ({verses})", callback_data=f"surah_{order}")])
    
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("◀️ Əvvəlki", callback_data=f"surahs_{page-1}"))
    if page + 1 < total_pages:
        nav_row.append(InlineKeyboardButton("Sonrakı ▶️", callback_data=f"surahs_{page+1}"))
    if nav_row:
        keyboard.append(nav_row)
    
    keyboard.append([InlineKeyboardButton("🏠 Əsas menyu", callback_data="main_menu")])
    
    msg = f"📖 *Surələr* ({page+1}/{total_pages})\n\nSurə adına klikləyin:"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_surah(update: Update, context: ContextTypes.DEFAULT_TYPE, surah_order: int, part: int = 0):
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['current_surah'] = surah_order
    user_data[user_id]['current_part'] = part
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name_az, verses_count FROM surahs WHERE order_no = ?", (surah_order,))
    surah = cursor.fetchone()
    if not surah:
        await update.callback_query.edit_message_text("❌ Surə tapılmadı!")
        return
    surah_id, surah_name, verses_count = surah
    
    per_part = 10
    offset = part * per_part
    cursor.execute('''SELECT verse_no, text_az, text_ar FROM verses WHERE surah_id = ? ORDER BY verse_no LIMIT ? OFFSET ?''', (surah_id, per_part, offset))
    verses = cursor.fetchall()
    conn.close()
    
    if not verses:
        await update.callback_query.edit_message_text("❌ Ayələr tapılmadı!")
        return
    
    total_parts = (verses_count + per_part - 1) // per_part
    start_verse = part * per_part + 1
    end_verse = min(start_verse + per_part - 1, verses_count)
    
    response = f"📖 *{surah_name} surəsi*\n📊 Hissə {part+1}/{total_parts} | Ayələr {start_verse}-{end_verse} / {verses_count}\n\n"
    for verse_no, text_az, text_ar in verses:
        if text_ar:
            response += f"*{verse_no}. {text_ar}*\n"
        response += f"_{text_az}_\n\n"
        if len(response) > 3800:
            response += "\n*... (davamı növbəti hissədə)*"
            break
    
    keyboard = []
    nav_row = []
    if part > 0:
        nav_row.append(InlineKeyboardButton("◀️ Əvvəlki hissə", callback_data=f"surah_part_{surah_order}_{part-1}"))
    if part + 1 < total_parts:
        nav_row.append(InlineKeyboardButton("Sonrakı hissə ▶️", callback_data=f"surah_part_{surah_order}_{part+1}"))
    if nav_row:
        keyboard.append(nav_row)
    
    row = []
    for verse_no, text_az, text_ar in verses:
        row.append(InlineKeyboardButton(str(verse_no), callback_data=f"verse_{surah_name}_{verse_no}"))
        if len(row) == 5:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    if total_parts <= 10:
        part_row = []
        for p in range(min(5, total_parts)):
            if p == part:
                part_row.append(InlineKeyboardButton(f"▪️{p+1}▪️", callback_data=f"surah_part_{surah_order}_{p}"))
            else:
                part_row.append(InlineKeyboardButton(f"{p+1}", callback_data=f"surah_part_{surah_order}_{p}"))
        if total_parts > 5:
            part_row.append(InlineKeyboardButton(f"...{total_parts}", callback_data=f"surah_part_{surah_order}_{total_parts-1}"))
        if part_row:
            keyboard.append(part_row)
    
    keyboard.append([InlineKeyboardButton("ℹ️ Surə haqqında", callback_data=f"info_{surah_order}")])
    keyboard.append([InlineKeyboardButton("🔙 Surələrə qayıt", callback_data=f"surahs_{user_data[user_id].get('surah_page', 0)}")])
    keyboard.append([InlineKeyboardButton("🏠 Əsas menyu", callback_data="main_menu")])
    
    await update.callback_query.edit_message_text(response, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_verse(update: Update, context: ContextTypes.DEFAULT_TYPE, surah_name: str, verse_no: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT s.order_no, v.text_az, v.text_ar FROM verses v JOIN surahs s ON v.surah_id = s.id WHERE s.name_az = ? AND v.verse_no = ?''', (surah_name, verse_no))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        await update.callback_query.edit_message_text("❌ Ayə tapılmadı!")
        return
    
    surah_order, text_az, text_ar = result
    
    response = f"📖 *{surah_name} surəsi, {verse_no}. ayə*\n\n"
    if text_ar:
        response += f"*{text_ar}*\n\n"
    response += f"_{text_az}_"
    
    keyboard = [
        [InlineKeyboardButton("🔊 Səsli oxu", callback_data=f"audio_{surah_order}_{verse_no}")],
        [InlineKeyboardButton("🔙 Surəyə qayıt", callback_data=f"surah_{surah_order}")],
        [InlineKeyboardButton("🏠 Əsas menyu", callback_data="main_menu")]
    ]
    
    await update.callback_query.edit_message_text(response, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== SURƏ MƏLUMATI ====================

async def surah_info(update: Update, context: ContextTypes.DEFAULT_TYPE, surah_order: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT name_az, name_ar, name_meaning, revelation_place, verses_count, summary FROM surahs WHERE order_no = ?''', (surah_order,))
    surah = cursor.fetchone()
    conn.close()
    
    if not surah:
        await update.callback_query.edit_message_text("❌ Məlumat tapılmadı!")
        return
    
    name_az, name_ar, meaning, revelation, verses, summary = surah
    info_text = f"📚 *{name_az} surəsi*\n\n🔤 *Ərəbcə:* {name_ar}\n📖 *Ayə sayı:* {verses}\n📍 *Nazil olduğu yer:* {revelation}\n💡 *Mənası:* {meaning}\n\n📝 *Məlumat:* {summary}"
    keyboard = [
        [InlineKeyboardButton("📖 Surəni oxu", callback_data=f"surah_{surah_order}")],
        [InlineKeyboardButton("🔙 Geri", callback_data=f"surahs_{user_data.get(update.effective_user.id, {}).get('surah_page', 0)}")]
    ]
    await update.callback_query.edit_message_text(info_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== TƏSADÜFİ AYƏ ====================

async def random_verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT s.name_az, v.verse_no, v.text_az, v.text_ar 
                      FROM verses v 
                      JOIN surahs s ON v.surah_id = s.id 
                      ORDER BY RANDOM() LIMIT 1''')
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        if update.callback_query:
            await update.callback_query.edit_message_text("❌ Ayə tapılmadı!")
        else:
            await update.message.reply_text("❌ Ayə tapılmadı!")
        return
    
    surah_name, verse_no, text_az, text_ar = result
    
    response = f"🌙 *Təsadüfi ayə*\n\n📖 *{surah_name} {verse_no}*\n\n"
    if text_ar:
        response += f"*{text_ar}*\n\n"
    response += f"_{text_az}_"
    
    keyboard = [
        [InlineKeyboardButton("🌙 Yeni ayə", callback_data="random")],
        [InlineKeyboardButton("🏠 Əsas menyu", callback_data="main_menu")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            response,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            response,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ==================== AUDIO (SƏSLİ AYƏ) ====================

def get_audio_from_db(surah_no, verse_no):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT audio_data FROM audio_cache WHERE surah_no = ? AND verse_no = ?", (surah_no, verse_no))
    result = cursor.fetchone()
    conn.close()
    if result:
        audio_file = BytesIO(result[0])
        audio_file.name = f"{surah_no}_{verse_no}.mp3"
        return audio_file
    return None

async def play_verse_audio(update: Update, context: ContextTypes.DEFAULT_TYPE, surah_no: int, verse_no: int):
    await update.callback_query.message.reply_text("⏳ Audio yüklənir...")
    audio_data = get_audio_from_db(surah_no, verse_no)
    if audio_data:
        await update.callback_query.message.reply_audio(
            audio=InputFile(audio_data),
            caption=f"🎧 {surah_no}:{verse_no}"
        )
    else:
        await update.callback_query.message.reply_text("❌ Audio tapılmadı!")

# ==================== ZİYARƏTLƏR ====================

async def ziyarat_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ziyarətlər menyusu"""
    keyboard = [
        [InlineKeyboardButton("📜 Ziyarəti-Əşura (Ərəbcə)", callback_data="ziyarat_ashura_ar")],
        [InlineKeyboardButton("📖 Ziyarəti-Əşura (Tərcümə)", callback_data="ziyarat_ashura_az")],
        [InlineKeyboardButton("🔙 Geri", callback_data="main_menu")]
    ]
    
    await update.callback_query.edit_message_text(
        "📜 *Ziyarətlər*\n\nZiyarət mətnini seçin:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_ziyarat_ashura_ar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ziyarəti-Əşuranı ərəbcə göstərir"""
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
    
    keyboard = [[InlineKeyboardButton("🔙 Ziyarətlərə qayıt", callback_data="ziyarat_menu")]]
    
    if len(content_ar) > 4000:
        await query.message.reply_text(
            f"📜 *Ziyarəti-Əşura (Ərəbcə)*\n\n{content_ar[:4000]}",
            parse_mode="Markdown"
        )
        await query.message.reply_text(
            content_ar[4000:8000],
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.message.reply_text(
            f"📜 *Ziyarəti-Əşura (Ərəbcə)*\n\n{content_ar}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def show_ziyarat_ashura_az(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ziyarəti-Əşuranı Azərbaycanca göstərir"""
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
    
    keyboard = [[InlineKeyboardButton("🔙 Ziyarətlərə qayıt", callback_data="ziyarat_menu")]]
    
    if len(content_az) > 4000:
        await query.message.reply_text(
            f"📖 *Ziyarəti-Əşura (Azərbaycanca)*\n\n{content_az[:4000]}",
            parse_mode="Markdown"
        )
        await query.message.reply_text(
            content_az[4000:8000],
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.message.reply_text(
            f"📖 *Ziyarəti-Əşura (Azərbaycanca)*\n\n{content_az}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ==================== BUTON HANDLER ====================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except:
        pass
    
    data = query.data
    
    try:
        if data == "main_menu":
            await main_menu(update, context)
            
        elif data == "hadiths":
            await hadiths_menu(update, context)
            
        elif data == "nahjul":
            await nahjul_menu(update, context)
            
        elif data == "bihar":
            await bihar_menu(update, context)
            
        elif data == "search":
            await search_prompt(update, context)
            
        elif data == "random":
            await random_verse(update, context)

        elif data == "ziyarat_menu":
            await ziyarat_menu(update, context)

        elif data == "ziyarat_ashura_ar":
            await show_ziyarat_ashura_ar(update, context)
            
        elif data == "ziyarat_ashura_az":
            await show_ziyarat_ashura_az(update, context)

        elif data == "gochat_click":
            await gochat_click_handler(update, context)

        elif data.startswith("audio_surahs_"):
            parts = data.split("_")
            page = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
            await show_audio_surahs(update, context, page)
            
        elif data.startswith("play_audio_"):
            parts = data.split("_")
            if len(parts) >= 3 and parts[2].isdigit():
                await play_surah_audio(update, context, int(parts[2]))
                
        elif data.startswith("surah_part_"):
            parts = data.split("_")
            if len(parts) >= 4 and parts[2].isdigit() and parts[3].isdigit():
                await show_surah(update, context, int(parts[2]), int(parts[3]))
                
        elif data.startswith("surah_"):
            parts = data.split("_")
            if len(parts) >= 2 and parts[1].isdigit():
                await show_surah(update, context, int(parts[1]), 0)
                
        elif data.startswith("verse_"):
            parts = data.split("_")
            if len(parts) >= 3:
                await show_verse(update, context, parts[1], parts[2])
                
        elif data.startswith("surahs_"):
            parts = data.split("_")
            page = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
            await show_surahs(update, context, page)
            
        elif data.startswith("info_"):
            parts = data.split("_")
            if len(parts) >= 2 and parts[1].isdigit():
                await surah_info(update, context, int(parts[1]))
                
        elif data.startswith("audio_"):
            parts = data.split("_")
            if len(parts) >= 3 and parts[1].isdigit():
                await play_verse_audio(update, context, int(parts[1]), parts[2])
                
        else:
            await query.edit_message_text(
                "❌ *Tanınmayan əmr!*",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 Əsas menyu", callback_data="main_menu")]
                ])
            )
            
    except Exception as e:
        print(f"❌ Button handler xətası: {e}")
        traceback.print_exc()
        try:
            await query.edit_message_text(
                f"❌ *Xəta!*\n\n{str(e)[:100]}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 Əsas menyu", callback_data="main_menu")]
                ])
            )
        except:
            pass

# ==================== MAIN ====================

def main():
    if not TOKEN:
        print("❌ Token tapılmadı!")
        return
    
    print("🚀 Quran Bot başladılır...")
    print(f"📊 Database: {DB_PATH}")
    
    app = Application.builder().token(TOKEN).connect_timeout(120.0).read_timeout(120.0).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("gochat", gochat))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Bot işə hazırdır!")
    print("🌐 Telegram-da botunuza /start yazın")
    
    app.run_polling()

if __name__ == "__main__":
    main()