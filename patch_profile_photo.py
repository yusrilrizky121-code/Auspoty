import re, os

base = r'C:\Users\Admin\Downloads\Auspoty'
js_path = os.path.join(base, 'public', 'script.js')

with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Ganti openEditProfile - tambah load foto custom
old = re.search(r'function openEditProfile\(\).*?^}', content, re.DOTALL | re.MULTILINE)
if old:
    new_fn = '''function openEditProfile() {
    const s = getSettings();
    const user = getGoogleUser();
    document.getElementById('editProfileName').value = s.profileName || (user ? user.name : '');
    const av = document.getElementById('editProfileAvatar');
    const customPhoto = localStorage.getItem('auspotyCustomPhoto');
    if (av) {
        if (customPhoto) {
            av.innerHTML = '<img src="' + customPhoto + '" style="width:100%;height:100%;object-fit:cover;">';
        } else if (user && user.picture) {
            av.innerHTML = '<img src="' + user.picture + '" style="width:100%;height:100%;object-fit:cover;">';
        } else {
            av.innerText = (s.profileName || 'A').charAt(0).toUpperCase();
        }
    }
    document.getElementById('editProfileModal').style.display = 'flex';
}'''
    content = content[:old.start()] + new_fn + content[old.end():]
    print("openEditProfile OK")
else:
    print("openEditProfile TIDAK DITEMUKAN")

# 2. Ganti saveProfile - simpan foto custom juga
old2 = re.search(r'function saveProfile\(\).*?^}', content, re.DOTALL | re.MULTILINE)
if old2:
    new_save = '''function saveProfile() {
    const name = document.getElementById('editProfileName').value.trim() || 'Pengguna Auspoty';
    saveSettings({ profileName: name });
    applyAllSettings();
    updateProfileUI();
    closeEditProfile();
    showToast('Profil disimpan!');
}'''
    content = content[:old2.start()] + new_save + content[old2.end():]
    print("saveProfile OK")
else:
    print("saveProfile TIDAK DITEMUKAN")

# 3. Tambah fungsi previewProfilePhoto setelah saveProfile
insert_after = 'function saveProfile() {'
idx = content.find(insert_after)
# cari akhir fungsi saveProfile
end_idx = content.find('\n}', idx) + 2

new_preview = '''

function previewProfilePhoto(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        const dataUrl = e.target.result;
        localStorage.setItem('auspotyCustomPhoto', dataUrl);
        const av = document.getElementById('editProfileAvatar');
        if (av) av.innerHTML = '<img src="' + dataUrl + '" style="width:100%;height:100%;object-fit:cover;">';
        updateProfileUI();
        showToast('Foto profil diperbarui!');
    };
    reader.readAsDataURL(file);
}'''

content = content[:end_idx] + new_preview + content[end_idx:]
print("previewProfilePhoto OK")

# 4. Update updateProfileUI - gunakan customPhoto jika ada
old3 = re.search(r'function updateProfileUI\(\).*?^}(?=\s*\nfunction logoutFromGoogle)', content, re.DOTALL | re.MULTILINE)
if old3:
    new_ui = '''function updateProfileUI() {
    const user = getGoogleUser();
    const s = getSettings();
    const customPhoto = localStorage.getItem('auspotyCustomPhoto');
    const loginBtn = document.getElementById('googleLoginBtn');
    const logoutBtn = document.getElementById('googleLogoutBtn');

    // Tentukan foto dan nama yang dipakai
    const displayName = user ? user.name : (s.profileName || 'Pengguna Auspoty');
    const displayPhoto = customPhoto || (user ? user.picture : null);

    // Update avatar settings
    const av = document.getElementById('settingsAvatar');
    if (av) {
        if (displayPhoto) {
            av.innerHTML = '<img src="' + displayPhoto + '" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
        } else {
            av.innerText = displayName.charAt(0).toUpperCase();
        }
    }
    const pname = document.getElementById('settingsProfileName');
    if (pname) pname.innerText = displayName;

    // Update home avatar
    const homeAv = document.querySelector('.app-avatar');
    if (homeAv) {
        if (displayPhoto) {
            homeAv.innerHTML = '<img src="' + displayPhoto + '" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
        } else {
            homeAv.innerText = displayName.charAt(0).toUpperCase();
        }
    }

    if (user) {
        const psub = document.getElementById('settingsProfileSub');
        if (psub) psub.innerText = user.email;
        const logoutSub = document.getElementById('googleLogoutSub');
        if (logoutSub) logoutSub.innerText = user.email;
        if (loginBtn) loginBtn.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'block';
    } else {
        const psub = document.getElementById('settingsProfileSub');
        if (psub) psub.innerText = 'Auspoty Premium';
        if (loginBtn) loginBtn.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'none';
    }
}'''
    content = content[:old3.start()] + new_ui + content[old3.end():]
    print("updateProfileUI OK")
else:
    print("updateProfileUI TIDAK DITEMUKAN - coba tanpa lookahead")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SELESAI")
