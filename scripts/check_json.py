import json
import os

def check_json():
    json_path = 'data/quran_complete.json'
    
    if not os.path.exists(json_path):
        print(f"❌ JSON faylı tapılmadı: {json_path}")
        return
    
    print("🚀 JSON faylı yoxlanılır...")
    print(f"📁 Fayl: {json_path}\n")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 JSON-da {len(data)} surə var\n")
    
    # Problemli surələri tapmaq üçün
    issues = []
    correct_names = []
    
    # Bütün surələri yoxla
    for i, (surah_name, verses) in enumerate(data.items(), 1):
        is_ok = True
        
        # 1. Ad yoxlaması
        if "surəsi" not in surah_name:
            issues.append(f"⚠️ {i}. surə: '{surah_name}' - adında 'surəsi' sözü yoxdur")
            is_ok = False
        
        # 2. Ayə sayı yoxlaması
        verse_count = len(verses)
        if verse_count == 0:
            issues.append(f"❌ {i}. surə: '{surah_name}' - heç bir ayə yoxdur!")
            is_ok = False
        elif verse_count < 3:
            issues.append(f"⚠️ {i}. surə: '{surah_name}' - cəmi {verse_count} ayə (çox az)")
        
        # 3. Ayə nömrələrinin ardıcıllığını yoxla
        verse_nums = sorted([int(v) for v in verses.keys()])
        expected_nums = list(range(1, verse_count + 1))
        
        if verse_nums != expected_nums:
            issues.append(f"⚠️ {i}. surə: '{surah_name}' - ayə nömrələri ardıcıl deyil!")
            issues.append(f"   Gözlənilən: 1-{verse_count}, Mövcud: {verse_nums[:5]}...")
            is_ok = False
        
        # 4. Ayə mətnlərinin boş olub olmadığını yoxla
        empty_verses = []
        for v_num, v_text in verses.items():
            if not v_text.strip():
                empty_verses.append(v_num)
        if empty_verses:
            issues.append(f"⚠️ {i}. surə: '{surah_name}' - {len(empty_verses)} ayənin mətni boşdur: {empty_verses[:5]}")
            is_ok = False
        
        if is_ok:
            correct_names.append((i, surah_name, verse_count))
    
    # Nəticələri göstər
    print("=" * 60)
    print("✅ DÜZGÜN SURƏLƏR:")
    print("=" * 60)
    for order, name, verses in correct_names[:20]:
        print(f"   {order:3}. {name:30} - {verses:3} ayə")
    if len(correct_names) > 20:
        print(f"   ... və {len(correct_names) - 20} surə daha")
    
    if issues:
        print("\n" + "=" * 60)
        print("⚠️ PROBLEMLİ SURƏLƏR:")
        print("=" * 60)
        for issue in issues:
            print(f"   {issue}")
    
    print("\n" + "=" * 60)
    print("📊 ÜMUMİ STATİSTİKA:")
    print("=" * 60)
    print(f"   Ümumi surə sayı: {len(data)}")
    print(f"   Düzgün surələr: {len(correct_names)}")
    print(f"   Problemli surələr: {len(issues)}")
    
    total_verses = sum(len(v) for v in data.values())
    print(f"   Ümumi ayə sayı: {total_verses}")
    
    # Ən uzun və ən qısa surələr
    longest = max(data.items(), key=lambda x: len(x[1]))
    shortest = min(data.items(), key=lambda x: len(x[1]))
    print(f"\n   📖 Ən uzun surə: {longest[0]} ({len(longest[1])} ayə)")
    print(f"   📖 Ən qısa surə: {shortest[0]} ({len(shortest[1])} ayə)")
    
    # Quran ardıcıllığını yoxla
    expected_order = [
        "Əl-Fatihə surəsi", "Əl-Bəqərə surəsi", "Ali-İmran surəsi",
        "Ən-Nisa surəsi", "Əl-Maidə surəsi", "Əl-Ənam surəsi"
    ]
    
    print("\n" + "=" * 60)
    print("📖 İLK 10 SURƏ (CARI SIRA):")
    print("=" * 60)
    for i, (name, verses) in enumerate(list(data.items())[:10], 1):
        print(f"   {i:2}. {name} ({len(verses)} ayə)")

if __name__ == "__main__":
    check_json()