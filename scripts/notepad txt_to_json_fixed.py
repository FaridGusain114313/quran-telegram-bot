# txt_to_json_fixed.py
import os
import json
import re

def convert_all_txt_to_json(txt_folder, json_path):
    all_surahs = []
    
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt') and f != 'quran_complete.json']
    txt_files.sort()
    
    for filename in txt_files:
        filepath = os.path.join(txt_folder, filename)
        surah_name = filename.replace('.txt', '').replace(' surəsi', '')
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        verses = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Yeni format: "19 De: Tərcümə" və ya "19 Tərcümə"
            # 1-ci format: "19 De: Tərcümə"
            match = re.match(r'^(\d+)\s+De:\s*(.+)$', line)
            if match:
                verse_no = int(match.group(1))
                translation = match.group(2)
                verses.append({'verse_no': verse_no, 'text_az': translation})
                continue
            
            # 2-ci format: "19 Tərcümə" (De: olmadan)
            match = re.match(r'^(\d+)\s+(.+)$', line)
            if match:
                verse_no = int(match.group(1))
                translation = match.group(2)
                verses.append({'verse_no': verse_no, 'text_az': translation})
                continue
            
            # 3-cü format: "1. Tərcümə"
            match = re.match(r'^(\d+)[.:\-]\s*(.+)$', line)
            if match:
                verse_no = int(match.group(1))
                translation = match.group(2)
                verses.append({'verse_no': verse_no, 'text_az': translation})
                continue
            
            # 4-cü format: "Bismillah..." (1-ci ayə)
            if not verses and line.startswith('Bismillah'):
                verses.append({'verse_no': 1, 'text_az': line})
                continue
            
            # Tanınmayan sətir - ama ayə ola bilər
            # Rəqəmlə başlayırsa, cəhd edək
            match = re.match(r'^(\d+)\s*', line)
            if match:
                verse_no = int(match.group(1))
                # Tərcüməni ayır
                translation = line[match.end():].strip()
                if translation:
                    verses.append({'verse_no': verse_no, 'text_az': translation})
                    continue
            
            # Heç bir format uyğun gəlmirsə, əvvəlki ayəyə əlavə et
            if verses:
                verses[-1]['text_az'] += ' ' + line
        
        all_surahs.append({
            'order_no': len(all_surahs) + 1,
            'name_az': surah_name,
            'verses': verses
        })
        
        print(f"✅ {surah_name}: {len(verses)} ayə")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_surahs, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON faylı yaradıldı: {json_path}")
    print(f"📊 Cəmi {len(all_surahs)} surə")

if __name__ == "__main__":
    txt_folder = r"C:\Users\Farid.Huseynzada\Desktop\Qurani-Kerim"
    json_path = "data/quran_complete.json"
    convert_all_txt_to_json(txt_folder, json_path)