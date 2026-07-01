import json

# Quran ardıcıllığı ilə surə adları
quran_order = [
    "Əl-Fatihə", "Əl-Bəqərə", "Ali-İmran", "Ən-Nisa", "Əl-Maidə",
    "Əl-Ənam", "Əl-Əraf", "Əl-Ənfal", "Ət-Tövbə", "Yunus",
    "Hud", "Yusif", "Ər-Rəd", "İbrahim", "Əl-Hicr",
    "Ən-Nəhl", "Əl-İsra", "Əl-Kəhf", "Məryəm", "Taha",
    "Əl-Ənbiya", "Əl-Həcc", "Əl-Muminun", "Ən-Nur", "Əl-Furqan",
    "Əş-Şuəra", "Ən-Nəml", "Əl-Qəsəs", "Əl-Ənkəbut", "Ər-Rum",
    "Loğman", "Əs-Səcdə", "Əl-Əhzab", "Səba", "Fatir",
    "Yasin", "Əs-Saffat", "Sad", "Əz-Zumər", "Əl-Mumin",
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

# JSON-u yüklə
with open('data/quran_complete.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Surələri adlarına görə axtar
new_data = []
for idx, name in enumerate(quran_order, 1):
    found = False
    for surah in data:
        if surah.get('name_az') == name:
            new_data.append({
                'order_no': idx,
                'name_az': surah.get('name_az'),
                'verses': surah.get('verses', [])
            })
            print(f"✅ {idx}. {name}")
            found = True
            break
    if not found:
        print(f"⚠️ {idx}. {name} - TAPILMADI!")

# Yeni JSON-a yaz
with open('data/quran_complete.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Surələr Quran ardıcıllığı ilə düzüldü! Cəmi: {len(new_data)} surə")