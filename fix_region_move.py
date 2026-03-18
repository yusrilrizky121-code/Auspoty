JS_PATH = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# Hapus HOME_QUERIES_BY_REGION dari posisi yang salah (dalam applyLanguageTitles)
# Cari dan hapus blok tersebut
import re

# Temukan blok HOME_QUERIES_BY_REGION yang ada sekarang
start_marker = '\nconst HOME_QUERIES_BY_REGION = {'
end_marker = '\n};\n'

idx_start = js.find(start_marker)
if idx_start == -1:
    print('ERROR: HOME_QUERIES_BY_REGION not found')
    exit()

# Cari closing }; setelah idx_start
idx_end = js.find(end_marker, idx_start)
if idx_end == -1:
    print('ERROR: closing }; not found')
    exit()

idx_end += len(end_marker)
old_region_block = js[idx_start:idx_end]
print('Found block at', idx_start, '-', idx_end)
print('Block preview:', repr(old_region_block[:100]))

# Hapus dari posisi lama
js = js[:idx_start] + js[idx_end:]
print('Removed from old position')

# Sekarang insert setelah HOME_QUERIES_BY_LANG closing
# HOME_QUERIES_BY_LANG diakhiri dengan "};\n" setelah Korean block
# Cari akhir HOME_QUERIES_BY_LANG
lang_start = js.find('const HOME_QUERIES_BY_LANG = {')
if lang_start == -1:
    print('ERROR: HOME_QUERIES_BY_LANG not found')
    exit()

# Cari closing }; dari HOME_QUERIES_BY_LANG
# Hitung bracket depth
depth = 0
i = lang_start
while i < len(js):
    if js[i] == '{':
        depth += 1
    elif js[i] == '}':
        depth -= 1
        if depth == 0:
            # Found closing brace
            # Skip to end of line (should be ';')
            end_lang = i + 1
            if end_lang < len(js) and js[end_lang] == ';':
                end_lang += 1
            if end_lang < len(js) and js[end_lang] == '\n':
                end_lang += 1
            break
    i += 1

print('HOME_QUERIES_BY_LANG ends at:', end_lang)
print('Context:', repr(js[end_lang-20:end_lang+50]))

# Insert HOME_QUERIES_BY_REGION setelah HOME_QUERIES_BY_LANG
region_block = """
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
"""

js = js[:end_lang] + region_block + js[end_lang:]
print('HOME_QUERIES_BY_REGION inserted after HOME_QUERIES_BY_LANG')

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

print('Done. File saved.')
