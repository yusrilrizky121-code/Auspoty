with open('public/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Cek baris 1-50 (top-level code yang dijalankan saat load)
print("=== TOP LEVEL CODE (non-function) ===")
in_func = 0
for i, line in enumerate(lines):
    stripped = line.strip()
    # Hitung depth
    for ch in line:
        if ch == '{': in_func += 1
        elif ch == '}': in_func -= 1
    # Baris top-level (depth 0) yang bukan komentar dan bukan kosong
    if in_func == 0 and stripped and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('*'):
        if not stripped.startswith('function ') and not stripped.startswith('async function ') and not stripped.startswith('class '):
            print(f"{i+1}: {stripped[:100]}")

print()
# Cek apakah ada 'let db' dan dbReq
print("=== DB INIT ===")
for i, line in enumerate(lines):
    if 'let db' in line or 'dbReq' in line or 'indexedDB' in line:
        print(f"{i+1}: {line.rstrip()[:100]}")
