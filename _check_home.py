with open('public/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Cari apiFetch
for i, line in enumerate(lines):
    if 'async function apiFetch' in line:
        for j in range(i, min(i+12, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
        print()
        break

# Cari loadHomeData
for i, line in enumerate(lines):
    if 'async function loadHomeData' in line:
        for j in range(i, min(i+30, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
