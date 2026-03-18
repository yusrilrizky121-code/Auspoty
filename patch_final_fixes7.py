with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari bagian updateProfileUI saat user null
i = content.find('function updateProfileUI')
print(repr(content[i:i+1500]))
