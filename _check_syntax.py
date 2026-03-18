with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Cek brace balance per baris — cari di mana balance jadi negatif
depth = 0
for i, line in enumerate(lines):
    # Skip string literals (kasar)
    for ch in line:
        if ch == '{': depth += 1
        elif ch == '}': depth -= 1
    if depth < 0:
        print(f"NEGATIVE DEPTH at line {i+1}: {line[:80]}")
        break

print(f"Final brace depth: {depth}")

# Cek apakah ada 'const HOME_QUERIES_BY_LANG' sebelum getHomeQueries
idx_lang = content.find('const HOME_QUERIES_BY_LANG')
idx_get = content.find('function getHomeQueries')
print(f"\nHOME_QUERIES_BY_LANG defined at char: {idx_lang}")
print(f"getHomeQueries defined at char: {idx_get}")
print(f"Order OK: {idx_lang < idx_get}")

# Cek apakah ada error di sekitar filterHome
idx_filter = content.find('function filterHome')
idx_load = content.find('async function loadSectionRows')
print(f"\nfilterHome at char: {idx_filter}")
print(f"loadSectionRows at char: {idx_load}")

# Cek apakah PODCAST_QUERIES didefinisikan sebelum filterHome
idx_podcast = content.find('const PODCAST_QUERIES')
print(f"PODCAST_QUERIES at char: {idx_podcast}")
print(f"PODCAST before filterHome: {idx_podcast < idx_filter}")
