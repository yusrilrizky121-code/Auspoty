with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari pola nama di HTML komentar
i = content.find("d.name + badge")
if i >= 0:
    print("Found at:", i)
    print(repr(content[i:i+300]))
else:
    # Cari alternatif
    i2 = content.find("d.name")
    while i2 >= 0:
        snippet = content[i2:i2+50]
        if 'badge' in snippet or 'ADMIN' in snippet:
            print("Found at:", i2, repr(snippet))
        i2 = content.find("d.name", i2+1)
