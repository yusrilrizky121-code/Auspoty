"""
Fix login di APK assets:
- script.js APK: loginWithGoogle() langsung buka LoginActivity, tidak ada modal
- index.html APK: hapus loginModal sama sekali
"""

import re, shutil

APK_ASSETS = r'C:\Users\Admin\Downloads\Auspoty\auspoty-apk\app\src\main\assets'

# ---- Fix script.js di APK assets ----
js_path = APK_ASSETS + r'\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Ganti seluruh blok GOOGLE LOGIN
old_block = re.compile(
    r'// ===================== GOOGLE LOGIN =====================.*?(?=\n// INIT)',
    re.DOTALL
)

new_block = """// ===================== GOOGLE LOGIN =====================
function loginWithGoogle() {
    const user = getGoogleUser();
    if (user) {
        if (confirm('Keluar dari akun ' + user.name + '?')) {
            localStorage.removeItem('auspotyGoogleUser');
            if (window.AndroidBridge) window.AndroidBridge.logout();
            updateProfileUI();
            showToast('Berhasil keluar');
        }
        return;
    }
    // Langsung buka LoginActivity — WebView Google login (cara Metrolist)
    if (window.AndroidBridge) {
        window.AndroidBridge.openGoogleLogin();
    }
}
function closeLoginModal() {}
function handleGoogleLogin(response) {}
function getGoogleUser() {
    try { return JSON.parse(localStorage.getItem('auspotyGoogleUser') || 'null'); } catch(e) { return null; }
}
function updateProfileUI() {
    const user = getGoogleUser();
    const s = getSettings();
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
        const loginText = document.getElementById('googleLoginText');
        if (loginText) loginText.innerText = 'Keluar dari Google';
        const loginSub = document.getElementById('googleLoginSub');
        if (loginSub) loginSub.innerText = user.email;
        const homeAv = document.querySelector('.app-avatar');
        if (homeAv) {
            if (user.picture) {
                homeAv.innerHTML = '<img src="' + user.picture + '" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
            } else {
                homeAv.innerText = user.name.charAt(0).toUpperCase();
            }
        }
    } else {
        const av = document.getElementById('settingsAvatar');
        if (av) av.innerText = (s.profileName || 'A').charAt(0).toUpperCase();
        const pname = document.getElementById('settingsProfileName');
        if (pname) pname.innerText = s.profileName || 'Pengguna Auspoty';
        const psub = document.getElementById('settingsProfileSub');
        if (psub) psub.innerText = 'Auspoty Premium';
        const loginText = document.getElementById('googleLoginText');
        if (loginText) loginText.innerText = 'Masuk dengan Google';
        const loginSub = document.getElementById('googleLoginSub');
        if (loginSub) loginSub.innerText = 'Sinkronkan data kamu';
    }
}

"""

if old_block.search(js):
    js = old_block.sub(new_block.strip(), js)
    print('APK script.js login block replaced OK')
else:
    marker = '// ===================== GOOGLE LOGIN ====================='
    init_marker = '\n// INIT'
    start = js.find(marker)
    end = js.find(init_marker)
    if start != -1 and end != -1:
        js = js[:start] + new_block.strip() + '\n' + js[end:]
        print('APK script.js replaced via manual find OK')
    else:
        print('ERROR: marker not found in APK script.js')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print('APK script.js saved')

# ---- Fix index.html di APK assets — hapus loginModal ----
html_path = APK_ASSETS + r'\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Hapus loginModal dan script GSI (tidak dibutuhkan di APK)
# Hapus tag script GSI
html = re.sub(r'\s*<script src="https://accounts\.google\.com/gsi/client"[^>]*></script>', '', html)

# Hapus loginModal block
modal_pattern = re.compile(
    r'\s*<!-- GOOGLE LOGIN MODAL -->.*?</div>\s*\n',
    re.DOTALL
)
if modal_pattern.search(html):
    html = modal_pattern.sub('\n', html)
    print('APK index.html loginModal removed OK')
else:
    # Coba cari manual
    start = html.find('<!-- GOOGLE LOGIN MODAL -->')
    end = html.find('</body>')
    if start != -1 and end != -1:
        # Hapus dari marker sampai sebelum </body>
        html = html[:start] + '\n' + html[end:]
        print('APK index.html loginModal removed via manual find OK')
    else:
        print('WARNING: loginModal not found in APK index.html')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('APK index.html saved')
print('\nDone! APK assets sudah difix.')
