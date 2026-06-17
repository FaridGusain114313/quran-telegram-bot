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
    "Yasin", "Əs-Saffat", "Sad", "Əz-Zumər", "Ğafir",
    "Fussilət", "Əş-Şura", "Əz-Zuxruf", "Əd-Duxan", "Əl-Casiyə",
    "Əl-Əhqaf", "Muhəmməd", "Əl-Fəth", "Əl-Hucurat", "Qaf",
    "Əz-Zariyat", "Ət-Tur", "Ən-Nəcm", "Əl-Qəmər", "Ər-Rəhman",
    "Əl-Vaqiə", "Əl-Hədid", "Əl-Mucadələ", "Əl-Həşr", "Əl-Mumtəhinə",
    "Əs-Saff", "Əl-Cumuə", "Əl-Munafiqun", "Ət-Təğabun", "Ət-Talaq",
    "Ət-Təhrim", "Əl-Mulk", "Nun", "Əl-Haqqə", "Əl-Məaric",
    "Nuh", "Əl-Cinn", "Əl-Muzzəmmil", "Əl-Muddəssir", "Əl-Qiyamə",
    "Əl-İnsan", "Əl-Mursəlat", "Ən-Nəbə", "Ən-Naziat", "Əbəsə",
    "Ət-Təkvir", "Əl-İnfitar", "Əl-Mutəffifin", "Əl-İnşiqaq", "Əl-Buruc",
    "Ət-Tariq", "Əl-Əla", "Əl-Ğaşiyə", "Əl-Fəcr", "Əl-Bələd",
    "Əş-Şəms", "Əl-Leyl", "Əz-Zuha", "Əl-İnşirah", "Ət-Tin",
    "Əl-Ələq", "Əl-Qədr", "Əl-Bəyyinə", "Əz-Zilzal", "Əl-Adiyat",
    "Əl-Qariə", "Ət-Təkasur", "Əl-Əsr", "Əl-Huməzə", "Əl-Fil",
    "Qureyş", "Əl-Maun", "Əl-Kovsər", "Əl-Kafirun", "Ən-Nəsr",
    "Əbu Ləhəb", "Əl-İxlas", "Əl-Fələq", "Ən-Nas"
]

def reset_and_reorder():
    print("🔄 Surələr yenidən sıralanır...")
    
    conn = sqlite3.connect('quran_bot.db')
    cursor = conn.cursor()
    
    # 1. Bütün surələrin order_no-larını müvəqqəti olaraq böyük rəqəmlərə çevir
    cursor.execute("SELECT id, name_az FROM surahs")
    surahs = cursor.fetchall()
    
    # 2. Hər surəyə düzgün order_no təyin et
    updated = 0
    not_found = []
    
    for order, correct_name in enumerate(correct_order, 1):
        found = False
        for surə_id, db_name in surahs:
            # Ad müqayisəsi (təmizlənmiş)
            clean_db_name = db_name.replace(" surəsi", "").strip()
            if clean_db_name == correct_name:
                cursor.execute("UPDATE surahs SET order_no = ? WHERE id = ?", (order, surə_id))
                print(f"  ✅ {order}. {clean_db_name}")
                updated += 1
                found = True
                break
        
        if not found:
            not_found.append(correct_name)
    
    # 3. Hələ də order_no təyin edilməmiş surələri tap
    cursor.execute("SELECT id, name_az FROM surahs WHERE order_no IS NULL")
    remaining = cursor.fetchall()
    
    if remaining:
        print(f"\n📌 Əlavə surələr (əl ilə yoxlanılmalı):")
        max_order = len(correct_order)
        for i, (surə_id, name) in enumerate(remaining, 1):
            clean_name = name.replace(" surəsi", "").strip()
            cursor.execute("UPDATE surahs SET order_no = ? WHERE id = ?", (max_order + i, surə_id))
            print(f"  ➕ {max_order + i}. {clean_name}")
    
    conn.commit()
    
    # 4. Yoxlama
    cursor.execute("SELECT order_no, name_az FROM surahs ORDER BY order_no LIMIT 20")
    print("\n📖 İLK 20 SURƏ (YENİ SIRA):")
    for order, name in cursor.fetchall():
        clean_name = name.replace(" surəsi", "").strip()
        print(f"   {order}. {clean_name}")
    
    cursor.execute("SELECT COUNT(*) FROM surahs WHERE order_no IS NULL")
    null_count = cursor.fetchone()[0]
    if null_count > 0:
        print(f"\n⚠️ Xəbərdarlıq: {null_count} surəyə sıra təyin edilməyib!")
    
    conn.close()
    
    print(f"\n✅ Tamamlandı! {updated} surə yeniləndi.")
    if not_found:
        print(f"⚠️ Tapılmayan surələr: {', '.join(not_found[:10])}")

if __name__ == "__main__":
    reset_and_reorder()