import os

BASE = r'C:\Users\Admin\Downloads\Auspoty'

# Fix index.html - viewport-fit=cover sudah ada, skip
with open(os.path.join(BASE, 'public', 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

if 'viewport-fit=cover' in html:
    print('viewport-fit=cover already present')
else:
    html = html.replace(
        'user-scalable=no"',
        'user-scalable=no, viewport-fit=cover"'
    )
    print('Added viewport-fit=cover')

with open(os.path.join(BASE, 'public', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html)

print('index.html DONE')
