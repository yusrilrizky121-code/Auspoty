js = open(r'C:\Users\Admin\Downloads\Auspoty\script_good.js','r',encoding='utf-16').read()
print('Lines:', js.count('\n'))
print('Brackets:', js.count('{'), js.count('}'))
idx = js.find('function applyAllSettings')
print('applyAllSettings found:', idx != -1)
if idx != -1:
    print(repr(js[idx:idx+300]))
