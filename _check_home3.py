with open('public/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Cari HOME_QUERIES_BY_REGION
for i, line in enumerate(lines):
    if 'HOME_QUERIES_BY_REGION' in line and ('const' in line or 'Indonesia' in line):
        for j in range(i, min(i+6, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
        print()
        break

# Cek apakah ada syntax error di sekitar baris 560-650
# Cek brace balance per fungsi
content = ''.join(lines)
# Cek apakah HOME_QUERIES_BY_REGION['Indonesia'] = null
idx = content.find('HOME_QUERIES_BY_REGION')
print("HOME_QUERIES_BY_REGION snippet:")
print(repr(content[idx:idx+200]))
