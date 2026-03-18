JS_PATH = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# ============ FIX 1: Font size - ganti block yang salah ============
# Cari dari "const sizes = {" sampai "});" berikutnya
import re

# Replace font size block
old1 = "    const sizes = { small: '13px', normal: '15px', large: '17px', xlarge: '20px' };\n    const sz = sizes[s.fontSize] || '15px';\n    document.documentElement.style.setProperty('--base-font-size', sz);\n    document.body.style.fontSize = sz;\n    // Apply ke semua elemen teks utama\n    document.querySelectorAll('.v-title,.h-title,.player-title,.settings-item-title,.lib-item-title').forEach(el => {\n        el.style.fontSize = '';\n    });"

new1 = "    // Font size via body class\n    document.body.classList.remove('font-small','font-normal','font-large','font-xlarge');\n    const fsMap = { small:'font-small', normal:'font-normal', large:'font-large', xlarge:'font-xlarge' };\n    document.body.classList.add(fsMap[s.fontSize] || 'font-normal');"

if old1 in js:
    js = js.replace(old1, new1)
    print('FIX1: font size block replaced OK')
else:
    print('FIX1: exact match not found, trying line by line...')
    lines = js.split('\n')
    new_lines = []
    skip = 0
    for i, line in enumerate(lines):
        if skip > 0:
            skip -= 1
            continue
        if "const sizes = { small: '13px'" in line:
            # skip next 6 lines (the whole block)
            new_lines.append("    // Font size via body class")
            new_lines.append("    document.body.classList.remove('font-small','font-normal','font-large','font-xlarge');")
            new_lines.append("    const fsMap = { small:'font-small', normal:'font-normal', large:'font-large', xlarge:'font-xlarge' };")
            new_lines.append("    document.body.classList.add(fsMap[s.fontSize] || 'font-normal');")
            skip = 6
        else:
            new_lines.append(line)
    js = '\n'.join(new_lines)
    print('FIX1: font size block replaced via line scan')

# ============ FIX 2: openLanguagePicker - reload home setelah ganti bahasa ============
old2 = "    ], s.language || 'Indonesia', (val) => { saveSettings({ language: val }); applyAllSettings(); });"
new2 = "    ], s.language || 'Indonesia', (val) => { const oldLang = getSettings().language; saveSettings({ language: val }); applyAllSettings(); if (oldLang !== val) loadHomeData(); });"

if old2 in js:
    js = js.replace(old2, new2)
    print('FIX2: language picker reload OK')
else:
    print('FIX2: language picker not found')

# ============ FIX 3: openRegionPicker - reload home setelah ganti wilayah ============
old3 = "    ], s.region || 'Indonesia', (val) => { saveSettings({ region: val }); applyAllSettings(); });"
new3 = "    ], s.region || 'Indonesia', (val) => { const oldRegion = getSettings().region; saveSettings({ region: val }); applyAllSettings(); if (oldRegion !== val) loadHomeData(); });"

if old3 in js:
    js = js.replace(old3, new3)
    print('FIX3: region picker reload OK')
else:
    print('FIX3: region picker not found')

# ============ FIX 4: HOME_QUERIES_BY_LANG - tambah region support ============
# Tambah HOME_QUERIES_BY_REGION setelah HOME_QUERIES_BY_LANG
region_queries = """
const HOME_QUERIES_BY_REGION = {
    Indonesia: null, // pakai HOME_QUERIES_BY_LANG
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
"""

if 'HOME_QUERIES_BY_REGION' not in js:
    # Insert after HOME_QUERIES_BY_LANG block
    insert_after = "    Korean: [\n        { id: 'rowAnyar',   query: 'kpop new songs 2025' },"
    # Find end of Korean block
    idx = js.find("    Korean: [")
    if idx != -1:
        # find closing '],' after Korean
        end_idx = js.find('];', idx)
        if end_idx != -1:
            end_idx = js.find('\n', end_idx) + 1
            end_idx = js.find('\n', end_idx) + 1  # skip closing }; of HOME_QUERIES_BY_LANG
            js = js[:end_idx] + region_queries + js[end_idx:]
            print('FIX4: HOME_QUERIES_BY_REGION added')
        else:
            print('FIX4: could not find end of Korean block')
    else:
        print('FIX4: Korean block not found')
else:
    print('FIX4: HOME_QUERIES_BY_REGION already exists')

# ============ FIX 5: getHomeQueries - pakai region juga ============
old5 = """function getHomeQueries() {
    const lang = getSettings().language || 'Indonesia';
    return HOME_QUERIES_BY_LANG[lang] || HOME_QUERIES_BY_LANG.Indonesia;
}"""

new5 = """function getHomeQueries() {
    const s = getSettings();
    const region = s.region || 'Indonesia';
    const lang = s.language || 'Indonesia';
    // Region override dulu, kalau ada
    if (HOME_QUERIES_BY_REGION && HOME_QUERIES_BY_REGION[region]) {
        return HOME_QUERIES_BY_REGION[region];
    }
    return HOME_QUERIES_BY_LANG[lang] || HOME_QUERIES_BY_LANG.Indonesia;
}"""

if old5 in js:
    js = js.replace(old5, new5)
    print('FIX5: getHomeQueries updated OK')
else:
    print('FIX5: getHomeQueries not found')

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

print('\nAll fixes applied. File saved.')
