import re

with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if already patched
if 'function getGoogleUser' in content:
    print('getGoogleUser already exists')
else:
    print('getGoogleUser MISSING - will add')

if 'function updateProfileUI' in content:
    print('updateProfileUI already exists')
else:
    print('updateProfileUI MISSING - will add')

# Find the // INIT block
init_idx = content.rfind('// INIT')
if init_idx == -1:
    print('ERROR: // INIT not found!')
    exit(1)

print(f'// INIT found at index {init_idx}')
print('Context:', repr(content[init_idx:init_idx+80]))

# Build the new functions to insert before INIT
new_funcs = '''
// GOOGLE USER HELPER
function getGoogleUser() {
    try { return JSON.parse(localStorage.getItem('auspotyGoogleUser') || 'null'); } catch(e) { return null; }
}

// UPDATE PROFILE UI
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
}

'''

# Only add if missing
insert = ''
if 'function getGoogleUser' not in content:
    insert += new_funcs
elif 'function updateProfileUI' not in content:
    # only add updateProfileUI
    insert += '''
// UPDATE PROFILE UI
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
}

'''

if insert:
    content = content[:init_idx] + insert + content[init_idx:]
    with open('public/script.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print('PATCHED OK - functions added before INIT')
else:
    print('No changes needed')
