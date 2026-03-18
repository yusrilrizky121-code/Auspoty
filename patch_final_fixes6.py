with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Inject deleteBtn setelah badge
old = "d.name+'</span>'+badge+'</div>"
new = "d.name+'</span>'+badge+deleteBtn+'</div>"

if old in content:
    content = content.replace(old, new)
    print("OK: deleteBtn injected")
else:
    print("WARN: not found")
    i = content.find("d.name+'")
    print(repr(content[i:i+100]))

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
