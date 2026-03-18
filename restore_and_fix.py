import os

GOOD = r'C:\Users\Admin\Downloads\Auspoty\script_good.js'
OUT  = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
CSS  = r'C:\Users\Admin\Downloads\Auspoty\public\style.css'

# Baca file bagus (UTF-16 karena PowerShell redirect)
js = open(GOOD, 'r', encoding='utf-16').read()
print('Base lines:', js.count('\n'), '| brackets:', js.count('{'), js.count('}'))

# ============================================================
# FIX 1: apiFetch fallback supaya home muncul di HP
# ============================================================
APIFETCH = '''
// API FETCH - fallback ke deployment aktif jika relative URL gagal
async function apiFetch(path) {
    try {
        const r = await fetch(path);
        if (r.ok) return r;
    } catch(e) {}
    return fetch('https://clone2-git-master-yusrilrizky121-codes-projects.vercel.app' + path);
}
'''

marker = 'let ytPlayer, isPlaying = false'
js = js.replace(marker, APIFETCH + marker, 1)

# Ganti semua fetch('/api/ dengan apiFetch('/api/
n = js.count("fetch('/api/")
js = js.replace("fetch('/api/", "apiFetch('/api/")
print(f'FIX1: apiFetch added, replaced {n} fetch calls')

# ============================================================
# FIX 2: Font size - ganti block sizes yang salah
# ============================================================
# Cari block lama
old_font = """    const sizes = { small: '13px', normal: '15px', large: '17px', xlarge: '20px' };
    const sz = sizes[s.fontSize] || '15px';
    document.documentElement.style.setProperty('--base-font-size', sz);
    document.body.style.fontSize = sz;
    // Apply ke semua elemen teks utama
    document.querySelectorAll('.v-title,.h-title,.player-title,.settings-item-title,.lib-item-title').forEach(el => {
        el.style.fontSize = '';
    });"""

new_font = """    // Font size via body class
    document.body.classList.remove('font-small','font-normal','font-large','font-xlarge');
    const fsMap = { small:'font-small', normal:'font-normal', large:'font-large', xlarge:'font-xlarge' };
    document.body.classList.add(fsMap[s.fontSize] || 'font-normal');"""

if old_font in js:
    js = js.replace(old_font, new_font)
    print('FIX2: font size block replaced OK')
else:
    # Coba cari versi tanpa comment
    old_font2 = "    const sizes = { small: '13px', normal: '15px', large: '17px', xlarge: '20px' };"
    if old_font2 in js:
        # Find and replace the whole block line by line
        lines = js.split('\n')
        new_lines = []
        skip = 0
        inserted = False
        for i, line in enumerate(lines):
            if skip > 0:
                skip -= 1
                continue
            if "const sizes = { small: '13px'" in line and not inserted:
                new_lines.append("    // Font size via body class")
                new_lines.append("    document.body.classList.remove('font-small','font-normal','font-large','font-xlarge');")
                new_lines.append("    const fsMap = { small:'font-small', normal:'font-normal', large:'font-large', xlarge:'font-xlarge' };")
                new_lines.append("    document.body.classList.add(fsMap[s.fontSize] || 'font-normal');")
                inserted = True
                skip = 6  # skip next 6 lines
            else:
                new_lines.append(line)
        js = '\n'.join(new_lines)
        print('FIX2: font size replaced via line scan')
    else:
        print('FIX2: WARNING - font size block not found')

# ============================================================
# FIX 3: Bahasa - reload home saat ganti bahasa
# ============================================================
old_lang = "    ], s.language || 'Indonesia', (val) => { saveSettings({ language: val }); applyAllSettings(); });"
new_lang = "    ], s.language || 'Indonesia', (val) => { saveSettings({ language: val }); applyAllSettings(); loadHomeData(); });"

if old_lang in js:
    js = js.replace(old_lang, new_lang)
    print('FIX3: language picker reload OK')
else:
    print('FIX3: language picker pattern not found - checking...')
    idx = js.find("openLanguagePicker")
    if idx != -1:
        print('  Found at:', repr(js[idx:idx+300]))

# ============================================================
# FIX 4: Wilayah - reload home saat ganti wilayah
# ============================================================
old_reg = "    ], s.region || 'Indonesia', (val) => { saveSettings({ region: val }); applyAllSettings(); });"
new_reg = "    ], s.region || 'Indonesia', (val) => { saveSettings({ region: val }); applyAllSettings(); loadHomeData(); });"

if old_reg in js:
    js = js.replace(old_reg, new_reg)
    print('FIX4: region picker reload OK')
else:
    print('FIX4: region picker pattern not found')

# ============================================================
# FIX 5: HOME_QUERIES_BY_LANG + REGION support
# ============================================================
# Cek apakah sudah ada
if 'HOME_QUERIES_BY_LANG' not in js:
    # Tambah setelah HOME_QUERIES
    HOME_EXTRA = """
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
const HOME_QUERIES_BY_REGION = {
    Indonesia: null,
    Global: [
        { id: 'rowAnyar',   query: 'top global songs 2025' },
        { id: 'rowGembira', query: 'happy pop songs 2025' },
        { id: 'rowCharts',  query: 'billboard hot 100 2025' },
        { id: 'rowGalau',   query: 'sad songs 2025' },
        { id: 'rowTiktok',  query: 'viral tiktok global 2025' },
        { id: 'rowHits',    query: 'trending songs worldwide 2025' },
    ],
    'Amerika Serikat': [
        { id: 'rowAnyar',   query: 'new american songs 2025' },
        { id: 'rowGembira', query: 'upbeat american pop 2025' },
        { id: 'rowCharts',  query: 'us top charts 2025' },
        { id: 'rowGalau',   query: 'sad american songs 2025' },
        { id: 'rowTiktok',  query: 'viral tiktok usa 2025' },
        { id: 'rowHits',    query: 'us trending songs today' },
    ],
    Jepang: [
        { id: 'rowAnyar',   query: 'japanese new songs 2025' },
        { id: 'rowGembira', query: 'japanese happy songs 2025' },
        { id: 'rowCharts',  query: 'japan oricon chart 2025' },
        { id: 'rowGalau',   query: 'japanese sad songs 2025' },
        { id: 'rowTiktok',  query: 'japan viral tiktok 2025' },
        { id: 'rowHits',    query: 'japanese trending today' },
    ],
    Korea: [
        { id: 'rowAnyar',   query: 'kpop new songs 2025' },
        { id: 'rowGembira', query: 'kpop happy songs 2025' },
        { id: 'rowCharts',  query: 'kpop melon chart 2025' },
        { id: 'rowGalau',   query: 'kpop sad songs 2025' },
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
"""
    # Insert setelah HOME_QUERIES array
    idx = js.find('const HOME_QUERIES = [')
    if idx != -1:
        end = js.find('];', idx) + 2
        js = js[:end] + HOME_EXTRA + js[end:]
        print('FIX5: HOME_QUERIES_BY_LANG/REGION added')
    else:
        print('FIX5: HOME_QUERIES not found')
else:
    print('FIX5: HOME_QUERIES_BY_LANG already exists')

# ============================================================
# FIX 6: getHomeQueries pakai lang + region
# ============================================================
old_ghq = """function getHomeQueries() {
    const lang = getSettings().language || 'Indonesia';
    return HOME_QUERIES_BY_LANG[lang] || HOME_QUERIES_BY_LANG.Indonesia;
}"""
new_ghq = """function getHomeQueries() {
    const s = getSettings();
    const region = s.region || 'Indonesia';
    const lang = s.language || 'Indonesia';
    if (typeof HOME_QUERIES_BY_REGION !== 'undefined' && HOME_QUERIES_BY_REGION[region]) {
        return HOME_QUERIES_BY_REGION[region];
    }
    if (typeof HOME_QUERIES_BY_LANG !== 'undefined') {
        return HOME_QUERIES_BY_LANG[lang] || HOME_QUERIES_BY_LANG.Indonesia;
    }
    return HOME_QUERIES;
}"""

if old_ghq in js:
    js = js.replace(old_ghq, new_ghq)
    print('FIX6: getHomeQueries updated')
else:
    print('FIX6: getHomeQueries not found (may already be updated)')

# ============================================================
# FIX 7: applyLanguageTitles pakai SECTION_TITLES_BY_LANG
# ============================================================
old_alt = """function applyLanguageTitles() {
    const lang = getSettings().language || 'Indonesia';
    const titles = SECTION_TITLES_BY_LANG[lang] || SECTION_TITLES_BY_LANG.Indonesia;
    const titleEls = document.querySelectorAll('.section-title');
    const titleMap = ['Sering','Rilis','Gembira','Tangga','Galau','Viral','Artis','Hit'];
    titleEls.forEach((el, i) => { if (titles[i]) el.innerText = titles[i]; });
}"""

if old_alt not in js:
    # Cari versi yang ada
    idx_alt = js.find('function applyLanguageTitles')
    if idx_alt != -1:
        end_alt = js.find('\n}', idx_alt) + 2
        old_block = js[idx_alt:end_alt]
        new_block = """function applyLanguageTitles() {
    const lang = getSettings().language || 'Indonesia';
    const titles = (typeof SECTION_TITLES_BY_LANG !== 'undefined' ? SECTION_TITLES_BY_LANG[lang] : null) || ['Sering kamu dengarkan','Rilis Anyar','Gembira & Semangat','Tangga Lagu Populer','Galau Terpopuler','Viral TikTok','Artis Terpopuler','Hit Hari Ini'];
    const titleEls = document.querySelectorAll('.section-title');
    titleEls.forEach((el, i) => { if (titles[i]) el.innerText = titles[i]; });
}"""
        js = js[:idx_alt] + new_block + js[end_alt:]
        print('FIX7: applyLanguageTitles updated')
    else:
        print('FIX7: applyLanguageTitles not found')
else:
    print('FIX7: applyLanguageTitles already correct')

# ============================================================
# Verifikasi akhir
# ============================================================
opens = js.count('{')
closes = js.count('}')
print(f'\nFinal: {js.count(chr(10))} lines, {{ {opens} }} {closes}, diff {opens-closes}')

open(OUT, 'w', encoding='utf-8').write(js)
print('Saved to', OUT)
