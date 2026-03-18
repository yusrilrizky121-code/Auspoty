import re

JS_PATH = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# Fix: applyLanguageTitles missing closing brace
old = """    titleEls.forEach((el, i) => { if (titles[i]) el.innerText = titles[i]; });

function applyUILanguage() {"""

new = """    titleEls.forEach((el, i) => { if (titles[i]) el.innerText = titles[i]; });
}

function applyUILanguage() {"""

if old in js:
    js = js.replace(old, new)
    print('FIXED: applyLanguageTitles missing closing brace')
else:
    print('Pattern not found, trying alternative...')
    # Try to find the exact pattern
    idx = js.find('titleEls.forEach((el, i) => { if (titles[i]) el.innerText = titles[i]; });')
    if idx != -1:
        after = js[idx+75:idx+120]
        print('After forEach:', repr(after))

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)
print('Saved.')
