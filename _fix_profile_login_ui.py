with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix 1: Setelah login sukses, panggil updateGoogleLoginUI juga
old1 = "          if (typeof updateProfileUI === 'function') updateProfileUI();\n          if (typeof showToast === 'function') showToast('Selamat datang, ' + userData.name.split(' ')[0] + '!');"
new1 = "          if (typeof updateProfileUI === 'function') updateProfileUI();\n          if (typeof updateGoogleLoginUI === 'function') updateGoogleLoginUI();\n          if (typeof showToast === 'function') showToast('Selamat datang, ' + userData.name.split(' ')[0] + '!');"

# Fix 2: Setelah logout, panggil updateGoogleLoginUI juga
old2 = "          if (typeof updateProfileUI === 'function') updateProfileUI();\n          if (typeof showToast === 'function') showToast('Berhasil keluar');"
new2 = "          if (typeof updateProfileUI === 'function') updateProfileUI();\n          if (typeof updateGoogleLoginUI === 'function') updateGoogleLoginUI();\n          if (typeof showToast === 'function') showToast('Berhasil keluar');"

# Fix 3: onAuthStateChanged juga panggil updateGoogleLoginUI
old3 = "          localStorage.setItem('auspotyGoogleUser', JSON.stringify(userData));\n          if (typeof updateProfileUI === 'function') updateProfileUI();\n        }\n      });"
new3 = "          localStorage.setItem('auspotyGoogleUser', JSON.stringify(userData));\n          if (typeof updateProfileUI === 'function') updateProfileUI();\n          if (typeof updateGoogleLoginUI === 'function') updateGoogleLoginUI();\n        }\n      });"

count = 0
if old1 in html:
    html = html.replace(old1, new1); count += 1; print('Fix 1 OK: login callback')
else:
    print('Fix 1 NOT FOUND')

if old2 in html:
    html = html.replace(old2, new2); count += 1; print('Fix 2 OK: logout callback')
else:
    print('Fix 2 NOT FOUND')

if old3 in html:
    html = html.replace(old3, new3); count += 1; print('Fix 3 OK: onAuthStateChanged')
else:
    print('Fix 3 NOT FOUND')

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'index.html: {count} fixes applied')

# Fix 4: updateProfileUI di script.js - custom photo harus prioritas di atas Google photo
with open('public/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_ui = """// UPDATE PROFILE UI
function updateProfileUI() {
    var user = getGoogleUser();
    var s = getSettings();
    var name = user ? user.name : (s.profileName || 'Pengguna Auspoty');
    var pic = user ? user.picture : (localStorage.getItem('auspotyCustomPhoto') || '');
    var pname = document.getElementById('settingsProfileName');
    if (pname) pname.innerText = name;
    var pav = document.getElementById('settingsAvatar');
    if (pav) {
        if (pic) { pav.innerHTML = '<img src="' + pic + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">'; }
        else { pav.innerHTML = ''; pav.innerText = name.charAt(0).toUpperCase(); }
    }
    var hav = document.querySelector('.app-avatar');
    if (hav) {
        if (pic) { hav.innerHTML = '<img src="' + pic + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">'; }
        else { hav.innerHTML = ''; hav.innerText = name.charAt(0).toUpperCase(); }
    }
}"""

new_ui = """// UPDATE PROFILE UI
function updateProfileUI() {
    var user = getGoogleUser();
    var s = getSettings();
    var name = user ? user.name : (s.profileName || 'Pengguna Auspoty');
    // Custom photo selalu prioritas, baru Google photo
    var customPhoto = localStorage.getItem('auspotyCustomPhoto');
    var pic = customPhoto || (user ? user.picture : '');
    var imgTag = pic ? '<img src="' + pic + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">' : '';
    var initial = name.charAt(0).toUpperCase();

    var pname = document.getElementById('settingsProfileName');
    if (pname) pname.innerText = name;

    var pav = document.getElementById('settingsAvatar');
    if (pav) {
        if (imgTag) { pav.innerHTML = imgTag; }
        else { pav.innerHTML = ''; pav.innerText = initial; }
    }
    var hav = document.querySelector('.app-avatar');
    if (hav) {
        if (imgTag) { hav.innerHTML = imgTag; }
        else { hav.innerHTML = ''; hav.innerText = initial; }
    }
}"""

if old_ui in js:
    js = js.replace(old_ui, new_ui)
    print('Fix 4 OK: updateProfileUI custom photo priority')
else:
    # try to find and patch differently
    print('Fix 4: trying fallback search...')
    idx = js.find('// UPDATE PROFILE UI')
    if idx != -1:
        print(f'Found at index {idx}, manual check needed')
        print(repr(js[idx:idx+300]))
    else:
        print('Fix 4 NOT FOUND')

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('DONE')
