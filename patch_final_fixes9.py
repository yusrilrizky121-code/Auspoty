with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

i = content.find('saveProfile')
print(repr(content[i:i+300]))
