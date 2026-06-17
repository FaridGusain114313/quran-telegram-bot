import sqlite3
import os
import sys

# Layihə kökünü əlavə et
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

def setup_database():
    """Database cədvəllərini yaradır"""
    
    db_path = os.getenv('DATABASE_PATH', 'quran_bot.db')
    
    # Schema faylını oxu
    schema_path = os.path.join('database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Database-ə qoşul
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Cədvəlləri yarat
    cursor.executescript(schema_sql)
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database yaradıldı: {db_path}")
    print("📊 Cədvəllər: surahs, verses, hadiths, tafsirs")

if __name__ == "__main__":
    setup_database()