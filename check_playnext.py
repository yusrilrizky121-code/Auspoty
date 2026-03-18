with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

i = content.find('function playNextSong')
print(repr(content[i:i+200]))

i2 = content.find('function playPrevSong')
print(repr(content[i2:i2+200]))
