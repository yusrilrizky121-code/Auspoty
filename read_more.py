with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari ENDED handler lengkap
i = content.find('PlayerState.ENDED')
print("=== ENDED full ===")
print(repr(content[i:i+400]))

# Cari playNextSimilarSong lengkap
i2 = content.find('async function playNextSimilarSong')
print("\n=== playNextSimilarSong full ===")
print(repr(content[i2:i2+600]))

# Cari home pills handler
with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
i3 = html.find('pill')
print("\n=== home pills HTML ===")
print(repr(html[i3-50:i3+400]))

# Cari podcast section
i4 = html.find('Podcast')
print("\n=== Podcast HTML ===")
print(repr(html[i4-50:i4+200]))
