import re

path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
content = open(path, 'r', encoding='utf-8').read()

print(f"File size: {len(content)} chars")

# Cek berapa kali function playMusic muncul
count = content.count('function playMusic(videoId, encodedData)')
print(f"function playMusic count: {count}")

# Cek window.currentTrack inject
idx = content.find('window.currentTrack = currentTrack;')
print(f"window.currentTrack at index: {idx}")
if idx > 0:
    print("Context around it:")
    print(repr(content[idx-300:idx+200]))
