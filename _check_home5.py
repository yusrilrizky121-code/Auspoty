with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cek semua const yang ada
import re
consts = re.findall(r'const (\w+)\s*=', content)
from collections import Counter
for name, count in Counter(consts).most_common():
    if 'HOME' in name or 'QUERY' in name or 'SECTION' in name or 'ARTIST' in name or 'PODCAST' in name:
        print(f"{name}: {count}x")

print()
# Cek apakah HOME_QUERIES_BY_LANG ada
print("HOME_QUERIES_BY_LANG:", 'const HOME_QUERIES_BY_LANG' in content)
print("HOME_QUERIES:", 'const HOME_QUERIES' in content)
print("SECTION_TITLES_BY_LANG:", 'const SECTION_TITLES_BY_LANG' in content)
print("PODCAST_QUERIES:", 'const PODCAST_QUERIES' in content)
print("PODCAST_TITLES:", 'const PODCAST_TITLES' in content)
print("ARTISTS:", 'const ARTISTS' in content)

# Cek apakah ada JS error obvious — cari baris yang punya syntax aneh
lines = content.split('\n')
for i, line in enumerate(lines[640:660], start=641):
    print(f"{i}: {line[:100]}")
