with open('public/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Cari getHomeQueries
for i, line in enumerate(lines):
    if 'function getHomeQueries' in line:
        for j in range(i, min(i+15, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
        print()
        break

# Cari HOME_QUERIES_BY_REGION — apakah Indonesia = null?
for i, line in enumerate(lines):
    if 'HOME_QUERIES_BY_REGION' in line and 'const' in line:
        for j in range(i, min(i+8, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
        print()
        break

# Cari INIT block — apakah loadHomeData dipanggil?
for i, line in enumerate(lines):
    if '// INIT' in line:
        for j in range(i, min(i+8, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
