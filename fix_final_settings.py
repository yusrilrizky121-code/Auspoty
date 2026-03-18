import re

css_path = r'C:\Users\Admin\Downloads\Auspoty\public\style.css'
js_path  = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'

# ── CSS: ganti semua font-size hardcoded di elemen teks utama pakai em/rem ──
with open(css_path, encoding='utf-8') as f:
    css = f.read()

# Elemen yang perlu scale dengan font size setting
replacements_css = [
    ('.v-title { font-size:15px;', '.v-title { font-size:1em;'),
    ('.v-sub { font-size:12px;',   '.v-sub { font-size:0.8em;'),
    ('.h-title { font-size:13px;', '.h-title { font-size:0.87em;'),
    ('.h-sub { font-size:12px;',   '.h-sub { font-size:0.8em;'),
    ('.lib-item-title { font-size:15px;', '.lib-item-title { font-size:1em;'),
    ('.lib-item-sub { font-size:12px;',   '.lib-item-sub { font-size:0.8em;'),
    ('.settings-item-title { font-size:15px;', '.settings-item-title { font-size:1em;'),
    ('.settings-item-sub { font-size:12px;',   '.settings-item-sub { font-size:0.8em;'),
    ('.mini-player-title { font-size:13px;', '.mini-player-title { font-size:0.87em;'),
    ('.mini-player-artist { font-size:11px;', '.mini-player-artist { font-size:0.73em;'),
    ('.section-title { font-size:20px;', '.section-title { font-size:1.33em;'),
]

changed_css = 0
for old, new in replacements_css:
    if old in css:
        css = css.replace(old, new)
        changed_css += 1

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
print(f"CSS: {changed_css} replacements done")

# ── JS: fix applyAllSettings font size ──
with open(js_path, encoding='utf-8') as f:
    js = f.read()

# Ganti blok font size yang ada
old_sz = """    const sizes = { small: '13px', normal: '15px', large: '17px', xlarge: '20px' };
    const sz = sizes[s.fontSize] || '15px';
    document.documentElement.style.setProperty('--base-font-size', sz);
    document.body.style.fontSize = sz;
    // Apply ke semua elemen teks utama
    document.querySelectorAll('.v-title,.h-title,.player-title,.settings-item-title,.lib-item-title').forEach(el => {
        el.style.fontSize = '';
    });"""

new_sz = """    const sizes = { small: '13px', normal: '15px', large: '18px', xlarge: '21px' };
    const sz = sizes[s.fontSize] || '15px';
    document.documentElement.style.setProperty('--base-font-size', sz);
    document.body.style.fontSize = sz;"""

if old_sz in js:
    js = js.replace(old_sz, new_sz)
    print("JS font size fix OK")
else:
    # fallback: cari dan ganti versi lama
    old_sz2 = "    const sizes = { small: '14px', normal: '16px', large: '18px', xlarge: '20px' };\n    document.documentElement.style.setProperty('--base-font-size', sizes[s.fontSize] || '16px');"
    new_sz2 = "    const sizes = { small: '13px', normal: '15px', large: '18px', xlarge: '21px' };\n    const sz = sizes[s.fontSize] || '15px';\n    document.documentElement.style.setProperty('--base-font-size', sz);\n    document.body.style.fontSize = sz;"
    if old_sz2 in js:
        js = js.replace(old_sz2, new_sz2)
        print("JS font size fallback fix OK")
    else:
        print("WARN: font size block not found, searching...")
        idx = js.find("--base-font-size")
        print("  found at:", idx, "context:", repr(js[max(0,idx-80):idx+60]))

# Fix bahasa: pastikan reload home saat bahasa berubah
if "saveSettings({ language: val }); applyAllSettings(); loadHomeData();" not in js:
    js = js.replace(
        "saveSettings({ language: val }); applyAllSettings();",
        "saveSettings({ language: val }); applyAllSettings(); loadHomeData();"
    )
    print("JS language reload fix OK")
else:
    print("JS language reload already OK")

# Fix wilayah: reload home saat region berubah + ubah query berdasarkan region
if "saveSettings({ region: val }); applyAllSettings(); loadHomeData();" not in js:
    js = js.replace(
        "saveSettings({ region: val }); applyAllSettings();",
        "saveSettings({ region: val }); applyAllSettings(); loadHomeData();"
    )
    print("JS region reload fix OK")
else:
    print("JS region reload already OK")

# Pastikan getHomeQueries pakai region juga
old_gq = """function getHomeQueries() {
    const lang = getSettings().language || 'Indonesia';
    return HOME_QUERIES_BY_LANG[lang] || HOME_QUERIES_BY_LANG.Indonesia;
}"""
new_gq = """function getHomeQueries() {
    const s = getSettings();
    const lang = s.language || 'Indonesia';
    const region = s.region || 'Indonesia';
    // Kalau region bukan Indonesia, paksa English queries
    if (region !== 'Indonesia' && lang === 'Indonesia') {
        return HOME_QUERIES_BY_LANG['English'] || HOME_QUERIES_BY_LANG.Indonesia;
    }
    return HOME_QUERIES_BY_LANG[lang] || HOME_QUERIES_BY_LANG.Indonesia;
}"""
if old_gq in js:
    js = js.replace(old_gq, new_gq)
    print("JS getHomeQueries region fix OK")
else:
    print("WARN: getHomeQueries not found as expected")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("ALL DONE")
