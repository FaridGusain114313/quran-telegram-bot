import json
import sqlite3
import os

DB_PATH = os.getenv('DATABASE_PATH', 'quran_bot.db')

def import_data():
    try:
        with open('data/quran_complete.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ JSON faylı tapılmadı!")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM verses")
    cursor.execute("DELETE FROM surahs")

    total_verses = 0
    surah_count = 0

    if isinstance(data, list):
        for surah_data in data:
            order_no = surah_data.get('order_no', 0)
            name_az = surah_data.get('name_az', f'{order_no}. surə')
            verses = surah_data.get('verses', [])

            if not verses:
                print(f"⚠️ {order_no}. {name_az} - ayələr yoxdur!")
                continue

            cursor.execute('''
                INSERT INTO surahs (order_no, name_az, verses_count)
                VALUES (?, ?, ?)
            ''', (order_no, name_az, len(verses)))

            surah_id = cursor.lastrowid
            surah_count += 1

            verse_count = 0
            seen_verses = set()

            for verse in verses:
                verse_no = verse.get('verse_no', 0)
                text_az = verse.get('text_az', '')
                text_ar = verse.get('text_ar', '')

                if verse_no == 0:
                    continue

                if verse_no in seen_verses:
                    continue
                seen_verses.add(verse_no)

                cursor.execute('''
                    INSERT INTO verses (surah_id, verse_no, text_az, text_ar)
                    VALUES (?, ?, ?, ?)
                ''', (surah_id, verse_no, text_az, text_ar))
                verse_count += 1
                total_verses += 1

            print(f"✅ {order_no}. {name_az}: {verse_count} ayə")

    conn.commit()
    conn.close()

    print("=" * 50)
    print(f"✅ İmport tamamlandı!")
    print(f"📊 {surah_count} surə, {total_verses} unikal ayə yükləndi")
    print("=" * 50)

if __name__ == "__main__":
    import_data()