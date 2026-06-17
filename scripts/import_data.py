import json
import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def import_surahs_from_json(json_path, db_path='quran_bot.db'):
    """JSON faylından surələri database-ə yükləyir"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for order, (surah_name, verses) in enumerate(data.items(), 1):
        # Surəni əlavə et
        cursor.execute('''
            INSERT OR REPLACE INTO surahs (order_no, name_az, verses_count)
            VALUES (?, ?, ?)
        ''', (order, surah_name, len(verses)))
        
        surah_id = cursor.lastrowid
        
        # Ayələri əlavə et
        for verse_no, text in verses.items():
            cursor.execute('''
                INSERT OR REPLACE INTO verses (surah_id, verse_no, text_az)
                VALUES (?, ?, ?)
            ''', (surah_id, verse_no, text))
    
    conn.commit()
    conn.close()
    
    print(f"✅ {len(data)} surə və {sum(len(v) for v in data.values())} ayə yükləndi")

if __name__ == "__main__":
    import_surahs_from_json('data/quran_complete.json')