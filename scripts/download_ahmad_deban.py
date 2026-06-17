import sqlite3
import os

audio_folder = "Quran_mp3"
db_path = "quran_bot.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS audio_surahs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surah_no INTEGER NOT NULL UNIQUE,
        audio_data BLOB NOT NULL
    )
''')

for i in range(1, 115):
    file_name = f"{i:03}.mp3"
    file_path = os.path.join(audio_folder, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            audio_blob = f.read()
        cursor.execute("INSERT OR REPLACE INTO audio_surahs (surah_no, audio_data) VALUES (?, ?)", (i, audio_blob))
        print(f"✅ {i}. surə əlavə edildi")
    else:
        print(f"❌ {i}. surə tapılmadı: {file_path}")

conn.commit()
conn.close()
print("\n✅ Bütün audio fayllar database-ə əlavə edildi!")