with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari history/popstate/back handling
i = content.find('popstate')
print("popstate:", repr(content[i:i+100]) if i>=0 else "NOT FOUND")

i2 = content.find('history.push')
print("history.push:", repr(content[i2:i2+100]) if i2>=0 else "NOT FOUND")

i3 = content.find('onKeyDown')
print("onKeyDown:", repr(content[i3:i3+100]) if i3>=0 else "NOT FOUND")

# Cari switchView untuk lihat apakah push history
i4 = content.find('function switchView')
print("\nswitchView:", repr(content[i4:i4+300]))
