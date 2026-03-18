import re, os

base = r'C:\Users\Admin\Downloads\Auspoty'
js_path = os.path.join(base, 'public', 'script.js')

with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

old = re.search(r'function applyAllSettings\(\).*?^}', content, re.DOTALL | re.MULTILINE)
if old:
    new_fn = """function applyAllSettings() {
    const s = getSettings();
    if (s.darkMode === false) document.body.classList.add('light-mode');
    else document.body.classList.remove('light-mode');

    // Tema warna — update --accent, --accent2, --spotify-green sekaligus
    const themes = {
        green:  { a: '#a78bfa', b: '#f472b6', g: '#a78bfa' },
        blue:   { a: '#38bdf8', b: '#818cf8', g: '#38bdf8' },
        red:    { a: '#f87171', b: '#fb923c', g: '#f87171' },
        purple: { a: '#c084fc', b: '#e879f9', g: '#c084fc' },
        orange: { a: '#fb923c', b: '#fbbf24', g: '#fb923c' },
    };
    const t = themes[s.theme] || themes.green;
    document.documentElement.style.setProperty('--accent', t.a);
    document.documentElement.style.setProperty('--accent2', t.b);
    document.documentElement.style.setProperty('--spotify-green', t.g);
    document.documentElement.style.setProperty('--spotify-green-dark', t.g);

    const sizes = { small: '14px', normal: '16px', large: '18px', xlarge: '20px' };
    document.documentElement.style.setProperty('--base-font-size', sizes[s.fontSize] || '16px');

    const themeNames = { green: 'Ungu-Pink (Default)', blue: 'Biru-Indigo', red: 'Merah-Oranye', purple: 'Ungu-Magenta', orange: 'Oranye-Kuning' };
    const el = document.getElementById('themeLabel'); if (el) el.innerText = themeNames[s.theme] || 'Ungu-Pink (Default)';
    const ql = document.getElementById('qualityLabel'); if (ql) ql.innerText = s.quality || 'Auto';
    const fl = document.getElementById('fontSizeLabel'); if (fl) fl.innerText = ({ small:'Kecil', normal:'Normal', large:'Besar', xlarge:'Sangat Besar' })[s.fontSize] || 'Normal';
    const ll = document.getElementById('langLabel'); if (ll) ll.innerText = s.language || 'Indonesia';
    const rl = document.getElementById('regionLabel'); if (rl) rl.innerText = s.region || 'Indonesia';
    setToggle('darkModeToggle', s.darkMode !== false);
    setToggle('autoplayToggle', s.autoplay !== false);
    setToggle('crossfadeToggle', !!s.crossfade);
    setToggle('normalizeToggle', !!s.normalize);
    setToggle('lyricsSyncToggle', s.lyricsSync !== false);
    setToggle('notifNowPlayingToggle', s.notifNowPlaying !== false);
    setToggle('notifNewReleaseToggle', !!s.notifNewRelease);
    const pname = document.getElementById('settingsProfileName'); if (pname) pname.innerText = s.profileName || 'Pengguna Auspoty';
    const pav = document.getElementById('settingsAvatar'); if (pav && !pav.querySelector('img')) pav.innerText = (s.profileName || 'A').charAt(0).toUpperCase();
    estimateCacheSize();
}"""
    content = content[:old.start()] + new_fn + content[old.end():]
    print("applyAllSettings OK")
else:
    print("TIDAK DITEMUKAN")

# Update juga openThemePicker label
old2 = re.search(r'function openThemePicker\(\).*?^}', content, re.DOTALL | re.MULTILINE)
if old2:
    new_picker = """function openThemePicker() {
    const s = getSettings();
    openPicker('Tema Warna', [
        { label: 'Ungu-Pink (Default)', value: 'green' },
        { label: 'Biru-Indigo', value: 'blue' },
        { label: 'Merah-Oranye', value: 'red' },
        { label: 'Ungu-Magenta', value: 'purple' },
        { label: 'Oranye-Kuning', value: 'orange' },
    ], s.theme || 'green', (val) => { saveSettings({ theme: val }); applyAllSettings(); });
}"""
    content = content[:old2.start()] + new_picker + content[old2.end():]
    print("openThemePicker OK")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SELESAI")
