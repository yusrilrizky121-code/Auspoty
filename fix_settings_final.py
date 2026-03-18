import re

JS_PATH = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
CSS_PATH = r'C:\Users\Admin\Downloads\Auspoty\public\style.css'

# ============ FIX 1: CSS font scaling ============
css_addition = """
/* FONT SIZE SCALING */
body.font-small  .v-title { font-size: 12px !important; }
body.font-small  .h-title { font-size: 11px !important; }
body.font-small  .section-title { font-size: 16px !important; }
body.font-small  .lib-item-title { font-size: 12px !important; }
body.font-small  .settings-item-title { font-size: 12px !important; }
body.font-small  .mini-player-title { font-size: 11px !important; }
body.font-small  .player-title { font-size: 18px !important; }
body.font-small  .v-sub, body.font-small .h-sub { font-size: 10px !important; }
body.font-large  .v-title { font-size: 17px !important; }
body.font-large  .h-title { font-size: 15px !important; }
body.font-large  .section-title { font-size: 23px !important; }
body.font-large  .lib-item-title { font-size: 17px !important; }
body.font-large  .settings-item-title { font-size: 17px !important; }
body.font-large  .mini-player-title { font-size: 15px !important; }
body.font-large  .player-title { font-size: 26px !important; }
body.font-large  .v-sub, body.font-large .h-sub { font-size: 14px !important; }
body.font-xlarge .v-title { font-size: 20px !important; }
body.font-xlarge .h-title { font-size: 17px !important; }
body.font-xlarge .section-title { font-size: 26px !important; }
body.font-xlarge .lib-item-title { font-size: 20px !important; }
body.font-xlarge .settings-item-title { font-size: 20px !important; }
body.font-xlarge .mini-player-title { font-size: 17px !important; }
body.font-xlarge .player-title { font-size: 30px !important; }
body.font-xlarge .v-sub, body.font-xlarge .h-sub { font-size: 15px !important; }
"""

with open(CSS_PATH, 'r', encoding='utf-8') as f:
    css = f.read()

if 'FONT SIZE SCALING' not in css:
    css += '\n' + css_addition
    with open(CSS_PATH, 'w', encoding='utf-8') as f:
        f.write(css)
    print('CSS: font scaling added')
else:
    print('CSS: already has font scaling')

# ============ FIX 2: applyAllSettings - fix font size + bahasa + wilayah ============
with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the broken font size block
old_font_block = """    const sizes = { small: '13px', normal: '15px', large: '17px', xlarge: '20px' };
    const sz = sizes[s.fontSize] || '15px';
    document.documentElement.style.setProperty('--base-font-size', sz);
    document.body.style.fontSize = sz;
    // Apply ke semua elemen teks utama
    document.querySelectorAll('.v-title,.h-title,.player-title,.settings-item-title,.lib-item-title').forEach(el => {
        el.style.fontSize = '';
    });"""

new_font_block = """    // Font size via body class
    document.body.classList.remove('font-small','font-normal','font-large','font-xlarge');
    const fsMap = { small:'font-small', normal:'font-normal', large:'font-large', xlarge:'font-xlarge' };
    document.body.classList.add(fsMap[s.fontSize] || 'font-normal');"""

if old_font_block in js:
    js = js.replace(old_font_block, new_font_block)
    print('JS: font size block replaced')
else:
    print('JS: font size block NOT found - trying partial match')
    # Try to find and replace just the sizes line
    if "const sizes = { small: '13px'" in js:
        # Find the block manually
        start = js.find("    const sizes = { small: '13px'")
        end = js.find("    });", start) + 6
        old_block = js[start:end]
        print(f'Found block: {repr(old_block[:100])}')
        js = js[:start] + new_font_block + js[end:]
        print('JS: font size block replaced (partial)')
    else:
        print('JS: font size block not found at all!')
