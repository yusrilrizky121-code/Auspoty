with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari applyLanguageTitles untuk sisipkan filterHome setelahnya
marker = "function applyLanguageTitles() {"
i = content.find(marker)
print("applyLanguageTitles at:", i)
print(repr(content[i:i+200]))

# Cari akhir fungsi applyLanguageTitles
end = content.find("\n}\n", i)
print("end at:", end)
print(repr(content[end:end+50]))
