import re, os

base = r'C:\Users\Admin\Downloads\Auspoty'
css_path = os.path.join(base, 'public', 'style.css')

with open(css_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Cari dari komentar SETTINGS sampai akhir .toggle-thumb active
old = re.search(r'/\* SETTINGS - Apple Music Style \*/.*?translateX\(20px\); \}', content, re.DOTALL)
if old:
    new_css = """/* SETTINGS */
.settings-header { padding:40px 16px 16px; position:sticky; top:0; background:var(--bg-base); z-index:50; }
.settings-header h1 { font-size:24px; font-weight:700; }
.settings-profile-card { margin:0 16px 8px; background:var(--bg-card); border-radius:12px; padding:16px; display:flex; align-items:center; gap:14px; cursor:pointer; transition:opacity .15s; }
.settings-profile-card:active { opacity:.7; }
.settings-avatar { width:52px; height:52px; border-radius:50%; background:linear-gradient(135deg,var(--spotify-green),var(--spotify-green-dark)); display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:800; color:#000; flex-shrink:0; overflow:hidden; }
.settings-profile-info { flex:1; }
.settings-profile-name { font-size:16px; font-weight:700; color:var(--text-main); margin-bottom:2px; }
.settings-profile-sub { font-size:13px; color:var(--spotify-green); font-weight:600; }
.settings-group-label { font-size:11px; font-weight:700; letter-spacing:1px; text-transform:uppercase; color:var(--text-sub); padding:20px 16px 8px; }
.settings-group { margin:0 16px; background:var(--bg-card); border-radius:12px; overflow:hidden; }
.settings-item { display:flex; align-items:center; justify-content:space-between; padding:14px 16px; border-bottom:1px solid rgba(255,255,255,.05); cursor:pointer; transition:background .15s; }
.settings-item:last-child { border-bottom:none; }
.settings-item:active { background:rgba(255,255,255,.05); }
.settings-item-left { display:flex; align-items:center; gap:14px; flex:1; }
.settings-icon { width:36px; height:36px; border-radius:8px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.settings-icon svg { fill:white; width:20px; height:20px; }
.settings-item-title { font-size:15px; font-weight:500; color:var(--text-main); margin-bottom:2px; }
.settings-item-sub { font-size:12px; color:var(--text-sub); }
.settings-chevron { fill:var(--text-sub); width:20px; height:20px; flex-shrink:0; }
.settings-toggle { width:48px; height:28px; border-radius:14px; background:rgba(255,255,255,.2); position:relative; cursor:pointer; transition:background .25s; flex-shrink:0; }
.settings-toggle.active { background:var(--spotify-green); }
.toggle-thumb { position:absolute; top:3px; left:3px; width:22px; height:22px; border-radius:50%; background:white; box-shadow:0 1px 4px rgba(0,0,0,.3); transition:transform .25s; }
.settings-toggle.active .toggle-thumb { transform:translateX(20px); }"""
    content = content[:old.start()] + new_css + content[old.end():]
    print("OK, reverted")
else:
    print("TIDAK DITEMUKAN, cari posisi...")
    idx = content.find('Apple Music')
    print("Apple Music di index:", idx)
    print("Sekitar:", repr(content[idx:idx+200]))

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SELESAI")
