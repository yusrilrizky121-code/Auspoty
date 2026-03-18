js_path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
with open(js_path, encoding='utf-8') as f:
    js = f.read()

# 1. FIX UKURAN TEKS - pastikan --base-font-size diterapkan ke body juga
old_size = "    const sizes = { small: '14px', normal: '16px', large: '18px', xlarge: '20px' };\n    document.documentElement.style.setProperty('--base-font-size', sizes[s.fontSize] || '16px');"
new_size = """    const sizes = { small: '13px', normal: '15px', large: '17px', xlarge: '20px' };
    const sz = sizes[s.fontSize] || '15px';
    document.documentElement.style.setProperty('--base-font-size', sz);
    document.body.style.fontSize = sz;
    // Apply ke semua elemen teks utama
    document.querySelectorAll('.v-title,.h-title,.player-title,.settings-item-title,.lib-item-title').forEach(el => {
        el.style.fontSize = '';
    });"""

if old_size in js:
    js = js.replace(old_size, new_size)
    print("font size fix OK")
else:
    print("WARN: font size old string not found")

# 2. FIX BAHASA - ubah query HOME_QUERIES dan CATEGORIES berdasarkan bahasa
# Tambah fungsi getLocalizedQuery sebelum HOME_QUERIES
old_home = "// HOME DATA\nconst HOME_QUERIES = ["
new_home = """// HOME DATA
const HOME_QUERIES_BY_LANG = {
    Indonesia: [
        { id: 'rowAnyar',   query: 'lagu indonesia terbaru 2025' },
        { id: 'rowGembira', query: 'lagu semangat gembira indonesia' },
        { id: 'rowCharts',  query: 'top hits indonesia 2025' },
        { id: 'rowGalau',   query: 'lagu galau sedih indonesia' },
        { id: 'rowTiktok',  query: 'viral tiktok indonesia 2025' },
        { id: 'rowHits',    query: 'lagu hits hari ini indonesia' },
    ],
    English: [
        { id: 'rowAnyar',   query: 'new english songs 2025' },
        { id: 'rowGembira', query: 'happy upbeat english songs' },
        { id: 'rowCharts',  query: 'top hits billboard 2025' },
        { id: 'rowGalau',   query: 'sad english songs' },
        { id: 'rowTiktok',  query: 'viral tiktok songs 2025' },
        { id: 'rowHits',    query: 'trending songs today' },
    ],
    Japanese: [
        { id: 'rowAnyar',   query: 'japanese new songs 2025' },
        { id: 'rowGembira', query: 'japanese happy songs' },
        { id: 'rowCharts',  query: 'japan top hits 2025' },
        { id: 'rowGalau',   query: 'japanese sad songs' },
        { id: 'rowTiktok',  query: 'japan viral tiktok 2025' },
        { id: 'rowHits',    query: 'japanese trending songs' },
    ],
    Korean: [
        { id: 'rowAnyar',   query: 'kpop new songs 2025' },
        { id: 'rowGembira', query: 'kpop happy songs' },
        { id: 'rowCharts',  query: 'kpop top hits 2025' },
        { id: 'rowGalau',   query: 'kpop sad songs' },
        { id: 'rowTiktok',  query: 'kpop viral tiktok 2025' },
        { id: 'rowHits',    query: 'kpop trending today' },
    ],
};
const SECTION_TITLES_BY_LANG = {
    Indonesia: ['Sering kamu dengarkan','Rilis Anyar','Gembira & Semangat','Tangga Lagu Populer','Galau Terpopuler','Viral TikTok','Artis Terpopuler','Hit Hari Ini'],
    English:   ['Recently Played','New Releases','Happy & Energetic','Top Charts','Sad Songs','Viral TikTok','Popular Artists','Hits Today'],
    Japanese:  ['最近再生','新着リリース','元気な曲','人気チャート','悲しい曲','バイラルTikTok','人気アーティスト','今日のヒット'],
    Korean:    ['최근 재생','신규 발매','신나는 노래','인기 차트','슬픈 노래','바이럴 틱톡','인기 아티스트','오늘의 히트'],
};
function getHomeQueries() {
    const lang = getSettings().language || 'Indonesia';
    return HOME_QUERIES_BY_LANG[lang] || HOME_QUERIES_BY_LANG.Indonesia;
}
function applyLanguageTitles() {
    const lang = getSettings().language || 'Indonesia';
    const titles = SECTION_TITLES_BY_LANG[lang] || SECTION_TITLES_BY_LANG.Indonesia;
    const titleEls = document.querySelectorAll('.section-title');
    const titleMap = ['Sering','Rilis','Gembira','Tangga','Galau','Viral','Artis','Hit'];
    titleEls.forEach((el, i) => { if (titles[i]) el.innerText = titles[i]; });
}
const HOME_QUERIES = ["""

if old_home in js:
    js = js.replace(old_home, new_home)
    print("home queries fix OK")
else:
    print("WARN: home queries old string not found")

# 3. Ganti loadHomeData untuk pakai getHomeQueries()
old_load = "    for (const row of HOME_QUERIES) {"
new_load = "    applyLanguageTitles();\n    for (const row of getHomeQueries()) {"

if old_load in js:
    js = js.replace(old_load, new_load)
    print("loadHomeData fix OK")
else:
    print("WARN: loadHomeData old string not found")

# 4. FIX WILAYAH - ubah query berdasarkan region
old_region_save = "    ], s.region || 'Indonesia', (val) => { saveSettings({ region: val }); applyAllSettings(); });"
new_region_save = "    ], s.region || 'Indonesia', (val) => { saveSettings({ region: val }); applyAllSettings(); loadHomeData(); });"

if old_region_save in js:
    js = js.replace(old_region_save, new_region_save)
    print("region reload fix OK")
else:
    print("WARN: region save old string not found")

# 5. Reload home saat bahasa berubah
old_lang_save = "    ], s.language || 'Indonesia', (val) => { saveSettings({ language: val }); applyAllSettings(); });"
new_lang_save = "    ], s.language || 'Indonesia', (val) => { saveSettings({ language: val }); applyAllSettings(); loadHomeData(); });"

if old_lang_save in js:
    js = js.replace(old_lang_save, new_lang_save)
    print("language reload fix OK")
else:
    print("WARN: language save old string not found")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("DONE")
