with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari HOME_QUERIES untuk tahu query podcast
i = content.find('const HOME_QUERIES_BY_LANG')
print("HOME_QUERIES_BY_LANG at:", i)

# Cari loadHomeData
i2 = content.find('async function loadHomeData')
print("loadHomeData at:", i2)
print(repr(content[i2:i2+200]))
