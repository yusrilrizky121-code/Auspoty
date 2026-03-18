with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix updateProfileUI - saat logout, tampilkan foto custom jika ada
old_logout_av = "    } else {\n        const av = document.getElementById('settingsAvatar'); if (av) av.innerText = (s.profileName||'A').charAt(0).toUpperCase();"

new_logout_av = """    } else {
        const av = document.getElementById('settingsAvatar');
        if (av) {
            const customPhoto = localStorage.getItem('auspotyCustomPhoto');
            if (customPhoto) {
                av.innerHTML = '<img src="'+customPhoto+'" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
            } else {
                av.innerHTML = '';
                av.innerText = (s.profileName||'A').charAt(0).toUpperCase();
            }
        }"""

if old_logout_av in content:
    content = content.replace(old_logout_av, new_logout_av)
    print("OK: updateProfileUI logout photo fixed")
else:
    print("WARN: not found")
    i = content.find("} else {")
    while i >= 0:
        snippet = content[i:i+100]
        if 'settingsAvatar' in snippet:
            print("Found at:", i, repr(snippet))
            break
        i = content.find("} else {", i+1)

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
