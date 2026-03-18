with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari playNextSimilarSong lengkap
i = content.find('async function playNextSimilarSong')
end = content.find('\nasync function ', i+1)
if end < 0:
    end = content.find('\nfunction ', i+1)
print("=== playNextSimilarSong ===")
print(repr(content[i:end]))

# Cari playMusic
i2 = content.find('function playMusic')
end2 = content.find('\nfunction ', i2+1)
print("\n=== playMusic ===")
print(repr(content[i2:end2]))

# Cari ENDED handler
i3 = content.find('PlayerState.ENDED')
print("\n=== ENDED handler ===")
print(repr(content[i3-20:i3+300]))
