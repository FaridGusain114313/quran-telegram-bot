import sqlite3
import requests
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def fetch_arabic_from_api():
    """
    alquran.cloud API-dən bütün ayələrin ərəbcə mətnlərini çəkir
    """
    print("🚀 Ərəbcə mətnlər API-dən yüklənir...")
    print("📡 Mənbə: alquran.cloud (pulsuz API)\n")
    
    conn = sqlite3.connect('quran_bot.db')
    cursor = conn.cursor()
    
    # Bütün surələri al (order_no sırası ilə)
    cursor.execute("SELECT id, order_no, name_az FROM surahs ORDER BY order_no")
    surahs = cursor.fetchall()
    
    print(f"📊 {len(surahs)} surə tapıldı\n")
    
    total_verses = 0
    success_count = 0
    
    for surah_id, surah_no, surah_name in surahs:
        print(f"[{surah_no:3}] 📖 {surah_name}...", end=' ')
        
        try:
            # API sorğusu
            url = f"https://api.alquran.cloud/v1/surah/{surah_no}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                verses = data['data']['ayahs']
                
                for verse in verses:
                    verse_no = verse['numberInSurah']
                    arabic_text = verse['text']
                    
                    cursor.execute('''
                        UPDATE verses 
                        SET text_ar = ? 
                        WHERE surah_id = ? AND verse_no = ?
                    ''', (arabic_text, surah_id, verse_no))
                    total_verses += 1
                
                conn.commit()
                success_count += 1
                print(f"✅ {len(verses)} ayə")
                
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("❌ Zaman aşımı")
        except Exception as e:
            print(f"❌ Xəta: {str(e)[:50]}")
        
        # Limitə riayət (saniyədə 10 sorğu)
        time.sleep(0.2)
    
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"✅ Yükləmə tamamlandı!")
    print(f"📊 Uğurlu surələr: {success_count}/{len(surahs)}")
    print(f"📝 Ümumi ayə: {total_verses}")
    print(f"📁 Database: quran_bot.db")
    print(f"{'='*50}")

def check_arabic_data():
    """Ərəbcə mətnlərin düzgün yükləndiyini yoxlayır"""
    conn = sqlite3.connect('quran_bot.db')
    cursor = conn.cursor()
    
    # Neçə ayədə ərəbcə mətn olduğunu yoxla
    cursor.execute("SELECT COUNT(*) FROM verses WHERE text_ar IS NOT NULL AND text_ar != ''")
    count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM verses")
    total = cursor.fetchone()[0]
    
    print(f"\n📊 Yoxlama nəticəsi:")
    print(f"   • Ümumi ayə: {total}")
    print(f"   • Ərəbcə mətn yüklənən: {count}")
    print(f"   • Qalan: {total - count}")
    
    if count == total:
        print("   ✅ Bütün ayələrə ərəbcə mətn yüklənib!")
    
    conn.close()

if __name__ == "__main__":
    fetch_arabic_from_api()
    check_arabic_data()