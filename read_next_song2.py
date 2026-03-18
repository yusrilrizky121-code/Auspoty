with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari playNextSimilarSong
i = content.find('async function playNextSimilarSong')
print("=== playNextSimilarSong ===")
# Cari sampai fungsi berikutnya
j = i + 1
depth = 0
for k in range(i, min(i+2000, len(content))):
    if content[k] == '{': depth += 1
    elif content[k] == '}':
        depth -= 1
        if depth == 0:
            j = k + 1
            break
print(repr(content[i:j]))

# Cari ENDED handler lengkap
i2 = content.find('PlayerState.ENDED')
print("\n=== ENDED full ===")
print(repr(content[i2:i2+400]))
