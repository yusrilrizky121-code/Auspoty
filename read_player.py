with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari onYouTubeIframeAPIReady dan player setup
i = content.find('onYouTubeIframeAPIReady')
print("=== YT Player setup ===")
print(repr(content[i:i+400]))

# Cari AudioContext keep-alive
i2 = content.find('_audioCtx')
print("\n=== AudioContext ===")
print(repr(content[i2:i2+600]))

# Cari visibilitychange
i3 = content.find('visibilitychange')
print("\n=== visibilitychange ===")
print(repr(content[i3:i3+400]))

# Cari progressInterval - ini yang mungkin berhenti
i4 = content.find('progressInterval')
print("\n=== progressInterval ===")
print(repr(content[i4:i4+200]))

# Cari startProgressBar
i5 = content.find('function startProgressBar')
print("\n=== startProgressBar ===")
print(repr(content[i5:i5+300]))
