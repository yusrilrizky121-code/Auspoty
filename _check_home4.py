with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari definisi HOME_QUERIES_BY_REGION
idx = content.find('const HOME_QUERIES_BY_REGION')
if idx == -1:
    print("HOME_QUERIES_BY_REGION NOT DEFINED!")
else:
    print("Found at char", idx)
    print(repr(content[idx:idx+300]))
