import re, os

base = r'C:\Users\Admin\Downloads\Auspoty'
css_path = os.path.join(base, 'public', 'style.css')

with open(css_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Hapus toggle lama (yang pakai spotify-green dan width:48px)
old_toggle = re.search(
    r'\.settings-toggle \{ width:48px.*?\.settings-toggle\.active \.toggle-thumb \{ transform:translateX\(20px\); \}',
    content, re.DOTALL
)
if old_toggle:
    content = content[:old_toggle.start()] + content[old_toggle.end():]
    print("Toggle lama dihapus OK")
else:
    print("Toggle lama tidak ditemukan")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SELESAI")
