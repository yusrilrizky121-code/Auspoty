with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari toggleRepeat dan onPlayerStateChange ENDED
i = content.find('toggleRepeat')
print("=== toggleRepeat ===")
print(repr(content[i:i+300]))

print("\n=== ENDED handler ===")
i2 = content.find('PlayerState.ENDED')
print(repr(content[i2-50:i2+300]))

print("\n=== playNextSimilarSong ===")
i3 = content.find('async function playNextSimilarSong')
print(repr(content[i3:i3+400]))

print("\n=== home pills ===")
i4 = content.find('pill')
print(repr(content[i4:i4+200]))
