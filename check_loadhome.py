with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

i = content.find('async function loadHomeData')
print(repr(content[i:i+800]))
