import sqlite3

conn = sqlite3.connect('quran_bot.db')
cursor = conn.cursor()

# CHECK constraint-i müvəqqəti sil
cursor.execute("DROP TRIGGER IF EXISTS check_revelation_place")
print("✅ CHECK constraint silindi")

# Bütün surələrin məlumatları
surah_data = {
    91: ('الشمس', 'Günəş (Şəms)', 'Məkkə', 'ŞƏMS surəsi günəşə, aya, gündüzə, gecəyə, göyə, yerə, nəfsə and içilməsindən bəhs edir.'),
    92: ('الليل', 'Gecə (Leyl)', 'Məkkə', 'LEYL surəsində gecəyə, gündüzə and içilməsi, insanların zəhmətinin cürbəcür olmasından bəhs edilir.'),
    93: ('الضحى', 'Günəş qalxdığı vaxt (Zuha)', 'Məkkə', 'ZUHA surəsində Rəbbinin Peyğəmbəri tərk etməməsi, ona nemət verməsindən bəhs edilir.'),
    94: ('الشرح', 'Köksü açma (İnşirah)', 'Məkkə', 'İNŞİRAH surəsində Allahın Peyğəmbərin köksünü açması, ağır yükünü götürməsindən bəhs edilir.'),
    95: ('التين', 'Əncir (Tin)', 'Məkkə', 'TİN surəsində əncirə, zeytuna, Tur dağına and içilməsi, insanın ən gözəl biçimdə yaradılmasından bəhs edilir.'),
    96: ('العلق', 'Laxtalanmış qan (Ələq)', 'Məkkə', 'ƏLƏQ surəsi Quranın ilk nazil olan surəsidir. "Oxu" əmri ilə başlayır.'),
    97: ('القدر', 'Qədr', 'Məkkə', 'QƏDR surəsində Quranın Qədr gecəsində nazil olması, bu gecənin min aydan xeyirli olmasından bəhs edilir.'),
    98: ('البينة', 'Açıq-aşkar dəlil (Bəyyinə)', 'Mədinə', 'BƏYYİNƏ surəsində kitab əhlindən kafirlər və müşriklər, iman gətirənlərin yaxşılığından bəhs edilir.'),
    99: ('الزلزلة', 'Zəlzələ (Zilzal)', 'Mədinə', 'ZİLZAL surəsində yerin lərzəyə gəlməsi, insanların əməllərinin göstərilməsindən bəhs edilir.'),
    100: ('العاديات', 'Çapar atlar (Adiyat)', 'Məkkə', 'ADİYAT surəsində atlara and içilməsi, insanın nankorluğundan bəhs edilir.'),
    101: ('القارعة', 'Qəhqəhəli qiyamət (Qariə)', 'Məkkə', 'QARİƏ surəsində qiyamətin dəhşəti, tərəzisi ağır gələnlərin xoş güzəranda olmasından bəhs edilir.'),
    102: ('التكاثر', 'Çoxluqla öyünmək (Təkasur)', 'Məkkə', 'TƏKASUR surəsində çoxluqla öyünməyin insanı qəflətə salmasından bəhs edilir.'),
    103: ('العصر', 'Axşam çağı (Əsr)', 'Məkkə', 'ƏSR surəsində insanın ziyanda olması, iman gətirib yaxşı işlər görənlərin isə nicat tapmasından bəhs edilir.'),
    104: ('الهمزة', 'Qeybət edən (Huməzə)', 'Məkkə', 'HUMƏZƏ surəsində qeybət edən, mal yığıb sayanların Cəhənnəmə atılacağından bəhs edilir.'),
    105: ('الفيل', 'Fil (Fil)', 'Məkkə', 'FİL surəsində fil sahiblərinin (Əbrəhə və ordusu) Kəbəni dağıtmaq istəyərkən məhv edilməsindən bəhs edilir.'),
    106: ('قريش', 'Qüreyş', 'Məkkə', 'QUREYŞ surəsində Qüreyş qəbiləsinin qış və yay səfərləri, Kəbənin Rəbbinə ibadət etmələrindən bəhs edilir.'),
    107: ('الماعون', 'Zəkat, xeyir (Maun)', 'Məkkə', 'MAUN surəsində dini yalan hesab edən, yetimi itələyən, yoxsulu yedirtməyən, namazında riyakarlıq edənlərin vəziyyətindən bəhs edilir.'),
    108: ('الكوثر', 'Kövsər', 'Məkkə', 'KÖVSƏR surəsində Allahın Peyğəmbərə Kövsər (Cənnətdə çay, bol nemət) bəxş etməsindən bəhs edilir.'),
    109: ('الكافرون', 'Kafirlər (Kafirun)', 'Məkkə', 'KAFİRUN surəsində kafirlərə: "Mən sizin ibadət etdiklərinizə ibadət etmərəm, sizin dininiz sizə, mənim dinim mənə" deyilməsi əmr edilir.'),
    110: ('النصر', 'Kömək (Nəsr)', 'Mədinə', 'NƏSR surəsində Allahın köməyi və zəfər (Məkkənin fəthi) gəldikdə Rəbbini təqdis etmək və Ondan bağışlanma diləmək əmr edilir.'),
    111: ('تبت', 'Əbu Ləhəb (Məsəd)', 'Məkkə', 'MƏSƏD surəsində Əbu Ləhəbin və onun övrətinin Cəhənnəmə gedəcəyi, mal-dövlətinin ona fayda verməyəcəyindən bəhs edilir.'),
    112: ('الإخلاص', 'İxlas', 'Məkkə', 'İXLAS surəsi Tövhid surəsidir. Allah birdir, heç kimə möhtac deyil, nə doğmuş, nə doğulmuşdur, Onun heç bir bənzəri yoxdur.'),
    113: ('الفلق', 'Dan yeri (Fələq)', 'Məkkə', 'FƏLƏQ surəsində sübhün Rəbbinə yaratdıqlarının, gecənin, cadugərlərin və paxılların şərindən pənah aparmaq əmr edilir.'),
    114: ('الناس', 'İnsanlar (Nas)', 'Məkkə', 'NAS surəsində insanların Rəbbinə, Hökmdarına, Tanrısına vəsvəsə verən Şeytanın şərindən pənah aparmaq əmr edilir.'),
}

for order, (name_ar, name_meaning, revelation, summary) in surah_data.items():
    cursor.execute('''
        UPDATE surahs 
        SET name_ar = ?, name_meaning = ?, revelation_place = ?, summary = ?
        WHERE order_no = ?
    ''', (name_ar, name_meaning, revelation, summary, order))
    print(f"✅ {order}. surə yeniləndi: {name_ar}")

conn.commit()
conn.close()

print("\n✅ 91-114-cü surələr uğurla yeniləndi!")

# Yoxlama
conn = sqlite3.connect('quran_bot.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM surahs WHERE name_ar IS NOT NULL AND name_ar != ''")
count = cursor.fetchone()[0]
print(f"\n📊 Yekun: {count}/114 surə məlumatı yükləndi")
if count == 114:
    print("🎉 TƏBRİKLƏR! BÜTÜN 114 SURƏNİN MƏLUMATLARI UĞURLA YÜKLƏNDİ!")
else:
    print(f"⚠️ {114 - count} surənin məlumatı yüklənməyib.")
conn.close()