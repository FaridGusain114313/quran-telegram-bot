import sqlite3
import os

def create_audio_table():
    db_path = 'quran_bot.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database tapılmadı: {db_path}")
        print("Əvvəlcə database-i yaradın: python scripts/setup_database.py")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            surah_no INTEGER NOT NULL,
            verse_no INTEGER NOT NULL,
            audio_data BLOB NOT NULL,
            reciter TEXT DEFAULT 'mishary',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(surah_no, verse_no, reciter)
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_audio_surah_verse ON audio_cache(surah_no, verse_no)')
    
    conn.commit()
    conn.close()
    
    print("✅ Audio cache cədvəli yaradıldı!")
    return True

if __name__ == "__main__":
    create_audio_table()