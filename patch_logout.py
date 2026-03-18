import re, os

base = r'C:\Users\Admin\Downloads\Auspoty'
js_path = os.path.join(base, 'public', 'script.js')

with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ganti updateProfileUI
old = re.search(r'function updateProfileUI\(\).*?^}', content, re.DOTALL | re.MULTILINE)
if old:
    new_func = '''function updateProfileUI() {
    const user = getGoogleUser();
    const s = getSettings();
    const loginBtn = document.getElementById('googleLoginBtn');
    const logoutBtn = document.getElementById('googleLogoutBtn');
    if (user) {
        const av = document.getElementById('settingsAvatar');
        if (av) {
            if (user.picture) {
                av.innerHTML = '<img src="' + user.picture + '" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
            } else {
                av.innerText = user.name.charAt(0).toUpperCase();
            }
        }
        const pname = document.getElementById('settingsProfileName');
        if (pname) pname.innerText = user.name;
        const psub = document.getElementById('settingsProfileSub');
        if (psub) psub.innerText = user.email;
        const logoutSub = document.getElementById('googleLogoutSub');
        if (logoutSub) logoutSub.innerText = user.email;
        const homeAv = document.querySelector('.app-avatar');
        if (homeAv) {
            if (user.picture) {
                homeAv.innerHTML = '<img src="' + user.picture + '" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
            } else {
                homeAv.innerText = user.name.charAt(0).toUpperCase();
            }
        }
        if (loginBtn) loginBtn.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'block';
    } else {
        const av = document.getElementById('settingsAvatar');
        if (av) av.innerText = (s.profileName || 'A').charAt(0).toUpperCase();
        const pname = document.getElementById('settingsProfileName');
        if (pname) pname.innerText = s.profileName || 'Pengguna Auspoty';
        const psub = document.getElementById('settingsProfileSub');
        if (psub) psub.innerText = 'Auspoty Premium';
        if (loginBtn) loginBtn.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'none';
    }
}

function logoutFromGoogle() {
    if (!confirm('Keluar dari akun Google?')) return;
    if (window._firebaseSignOut) {
        window._firebaseSignOut();
    } else {
        localStorage.removeItem('auspotyGoogleUser');
        updateProfileUI();
        showToast('Berhasil keluar');
    }
}'''
    content = content[:old.start()] + new_func + content[old.end():]
    print("updateProfileUI OK")
else:
    print("updateProfileUI TIDAK DITEMUKAN")

# Ganti loginWithGoogle - hapus logika logout di dalamnya
old2 = re.search(r'function loginWithGoogle\(\).*?^}', content, re.DOTALL | re.MULTILINE)
if old2:
    new_login = '''function loginWithGoogle() {
    const user = getGoogleUser();
    if (user) return;
    if (window._firebaseSignIn) {
        window._firebaseSignIn();
    } else {
        document.getElementById('loginModal').style.display = 'flex';
    }
}'''
    content = content[:old2.start()] + new_login + content[old2.end():]
    print("loginWithGoogle OK")
else:
    print("loginWithGoogle TIDAK DITEMUKAN")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SELESAI")
