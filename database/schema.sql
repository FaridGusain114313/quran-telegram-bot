-- Surələr cədvəli
CREATE TABLE IF NOT EXISTS surahs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_no INTEGER UNIQUE NOT NULL,
    name_az TEXT NOT NULL,
    name_ar TEXT,
    name_meaning TEXT,
    verses_count INTEGER DEFAULT 0,
    revelation_place TEXT CHECK(revelation_place IN ('Məkkə', 'Mədinə', 'Məlumat yoxdur')),
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ayələr cədvəli
CREATE TABLE IF NOT EXISTS verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    verse_no INTEGER NOT NULL,
    text_az TEXT NOT NULL,
    text_ar TEXT,
    juz_no INTEGER,
    hizb_no INTEGER,
    FOREIGN KEY (surah_id) REFERENCES surahs(id) ON DELETE CASCADE,
    UNIQUE(surah_id, verse_no)
);

-- Hədislər cədvəli
CREATE TABLE IF NOT EXISTS hadiths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    text_az TEXT NOT NULL,
    text_ar TEXT,
    source TEXT NOT NULL,
    book TEXT,
    hadith_no TEXT,
    grade TEXT CHECK(grade IN ('Səhih', 'Həsən', 'Zəif', 'Mövzu', 'Məlumat yoxdur')),
    category TEXT,
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Təfsir cədvəli (gələcək üçün)
CREATE TABLE IF NOT EXISTS tafsirs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    text_az TEXT NOT NULL,
    source TEXT,
    FOREIGN KEY (verse_id) REFERENCES verses(id) ON DELETE CASCADE
);

-- İndekslər (sürətli axtarış üçün)
CREATE INDEX IF NOT EXISTS idx_verses_surah ON verses(surah_id);
CREATE INDEX IF NOT EXISTS idx_verses_verse_no ON verses(verse_no);
CREATE INDEX IF NOT EXISTS idx_hadiths_category ON hadiths(category);
CREATE INDEX IF NOT EXISTS idx_hadiths_source ON hadiths(source);