# txt_to_json.py
import os
import json
import re

def convert_all_txt_to_json(txt_folder, json_path):
    """
    Hər surə üçün ayrı TXT faylını vahid JSON-a çevirir
    """
    all_surahs = []
    
    # Bütün TXT fayllarını al
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt') and f != 'quran_complete.json']
    
    # Faylları surə sırasına görə çeşidlə (rəqəmə görə)
    def get_surah_number(filename):
        # "Əl-Bəqərə surəsi.txt" → 2
        # "Ali-İmran surəsi.txt" → 3
        # Burada sadəcə fayl adına görə sıralayırıq
        # Əgər fayl adında rəqəm yoxdursa, sona qoy
        return 999
    
    # Əvvəlcə bütün faylları toplayaq
    for filename in sorted(txt_files):
        filepath = os.path.join(txt_folder, filename)
        
        # Surə adını fayl adından çıxar
        surah_name = filename.replace('.txt', '').replace(' surəsi', '')
        
        # TXT faylını oxu
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        verses = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Format: "1. Tərcümə" və ya "1: Tərcümə" və ya "1 - Tərcümə"
            match = re.match(r'^(\d+)[.:\-]\s*(.+)$', line)
            if match:
                verse_no = int(match.group(1))
                translation = match.group(2)
                verses.append({
                    'verse_no': verse_no,
                    'text_az': translation
                })
            else:
                # Format: "Bismillahir-rəhmanir-rəhim" (1-ci ayə üçün)
                if not verses:
                    verses.append({
                        'verse_no': 1,
                        'text_az': line
                    })
                else:
                    print(f"⚠️ {filename} - tanınmayan sətir: {line[:50]}...")
        
        # Əgər ayələr yoxdursa, əlavə etmə
        if not verses:
            print(f"⚠️ {filename} - heç bir ayə tapılmadı!")
            continue
        
        # Surəni əlavə et (order_no sonradan düzələcək)
        all_surahs.append({
            'name_az': surah_name,
            'name_ar': '',
            'verses': verses,
            'filename': filename
        })
        
        print(f"✅ {surah_name}: {len(verses)} ayə")
    
    # İndi surələri düzgün sıraya düzək (əl ilə və ya API ilə)
    # Sizin surələr artıq doğru sıradadır, sadəcə order_no əlavə edirik
    for idx, surah in enumerate(all_surahs, 1):
        surah['order_no'] = idx
    
    # JSON-a yaz
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_surahs, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON faylı yaradıldı: {json_path}")
    print(f"📊 Cəmi {len(all_surahs)} surə")

if __name__ == "__main__":
    # TXT fayllarının yeri
    txt_folder = r"C:\Users\Farid.Huseynzada\Desktop\Qurani-Kerim"
    json_path = "data/quran_complete.json"
    
    convert_all_txt_to_json(txt_folder, json_path)