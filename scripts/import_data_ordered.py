import sqlite3
import json

# Quranın düzgün surə sırası
correct_order = [
    "Əl-Fatihə", "Əl-Bəqərə", "Ali-İmran", "Ən-Nisa", "Əl-Maidə",
    "Əl-Ənam", "Əl-Əraf", "Əl-Ənfal", "Ət-Tövbə", "Yunus",
    "Hud", "Yusif", "Ər-Rəd", "İbrahim", "Əl-Hicr",
    "Ən-Nəhl", "Əl-İsra", "Əl-Kəhf", "Məryəm", "Taha",
    "Əl-Ənbiya", "Əl-Həcc", "Əl-Muminun", "Ən-Nur", "Əl-Furqan",
    "Əş-Şuəra", "Ən-Nəml", "Əl-Qəsəs", "Əl-Ənkəbut", "Ər-Rum",
    "Loğman", "Əs-Səcdə", "Əl-Əhzab", "Səba", "Fatir",
    "Yasin", "Əs-Saffat", "Sad", "Əz-Zumər", "Əl-Ğafir",
    "Fussilət", "Əş-Şura", "Əz-Zuxruf", "Əd-Duxan", "Əl-Casiyə",
    "Əl-Əhqaf", "Məhəmməd", "Əl-Fəth", "Əl-Hucurat", "Qaf",
    "Əz-Zariyat", "Ət-Tur", "Ən-Nəcm", "Əl-Qəmər", "Ər-Rəhman",
    "Əl-Vaqiə", "Əl-Hədid", "Əl-Mucadələ", "Əl-Həşr", "Əl-Mumtəhinə",
    "Əs-Səff", "Əl-Cumuə", "Əl-Munafiqun", "Ət-Təğabun", "Ət-Talaq",
    "Ət-Təhrim", "Əl-Mulk", "Nun", "Əl-Haqqə", "Əl-Məaric",
    "Nuh", "Əl-Cinn", "Əl-Muzzəmmil", "Əl-Muddəssir", "Əl-Qiyamə",
    "Əl-İnsan", "Əl-Mursəlat", "Ən-Nəbə", "Ən-Naziat", "Əbəsə",
    "Ət-Təkvir", "Əl-İnfitar", "Əl-Mutəffifin", "Əl-İnşiqaq", "Əl-Buruc",
    "Ət-Tariq", "Əl-Əla", "Əl-Ğaşiyə", "Əl-Fəcr", "Əl-Bələd",
    "Əş-Şəms", "Əl-Leyl", "Əz-Zuha", "Əl-İnşirah", "Ət-Tin",
    "Əl-Ələq", "Əl-Qədr", "Əl-Bəyyinə", "Əz-Zilzal", "Əl-Adiyat",
    "Əl-Qariə", "Ət-Təkasur", "Əl-Əsr", "Əl-Huməzə", "Əl-Fil",
    "Əl-Qureyş", "Əl-Maun", "Əl-Kovsər", "Əl-Kafirun", "Ən-Nəsr",
    "Əbu Ləhəb", "Əl-İxlas", "Əl-Fələq", "Ən-Nas"
]

def import_ordered():
    print("🚀 Surələr düzgün sıra ilə import edilir...")
    
    # JSON faylını yüklə
    with open('data/quran_complete.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Adları təmizlə: JSON-da "Əl-Fatihə surəsi" kimi yazılıb
    surah_map = {}
    for key, value in data.items():
        clean_name = key.replace(" surəsi", "").strip()
        surah_map[clean_name] = value
    
    conn = sqlite3.connect('quran_bot.db')
    cursor = conn.cursor()
    
    total_verses = 0
    
    for order, surah_name in enumerate(correct_order, 1):
        if surah_name in surah_map:
            verses = surah_map[surah_name]
            
            # Surəni əlavə et
            cursor.execute('''
                INSERT INTO surahs (order_no, name_az, verses_count)
                VALUES (?, ?, ?)
            ''', (order, surah_name, len(verses)))
            
            surah_id = cursor.lastrowid
            
            # Ayələri əlavə et
            for verse_no, text in verses.items():
                cursor.execute('''
                    INSERT INTO verses (surah_id, verse_no, text_az)
                    VALUES (?, ?, ?)
                ''', (surah_id, verse_no, text))
                total_verses += 1
            
            print(f"✅ {order}. {surah_name} - {len(verses)} ayə")
        else:
            print(f"⚠️ {order}. {surah_name} - JSON-da tapılmadı!")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"✅ İmport tamamlandı!")
    print(f"📊 {len(correct_order)} surə, {total_verses} ayə yükləndi")
    print(f"📁 Surələr Quran ardıcıllığı ilə düzülüb")
    print(f"{'='*50}")

if __name__ == "__main__":
    import_ordered()