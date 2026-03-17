import re

js_path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

old_block = re.compile(
    r'// ===================== GOOGLE LOGIN =====================.*?(?=\n// INIT)',
    re.DOTALL
)

new_block = """// ===================== GOOGLE LOGIN =====================
// Cara login persis seperti Metrolist:
// Buka WebView ke accounts.google.com → user login → redirect ke music.youtube.com → ambil cookie
// Tidak perlu Google Cloud Console / OAuth setup apapun.
const GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'; // hanya untuk web fallback

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
    // Di APK Android: buka LoginActivity (WebView Google login seperti Metrolist)
    if (window.AndroidBridge && window.AndroidBridge.isAndroid()) {
        window.AndroidBridge.openGoogleLogin();
    } else {
        // Di web: tampilkan modal GSI
        _showLoginModal();
    }
}

function _showLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.style.display = 'flex';
    if (window.google && window.google.accounts && GOOGLE_CLIENT_ID !== 'YOUR_GOOGLE_CLIENT_ID') {
        try {
            google.accounts.id.initialize({
                client_id: GOOGLE_CLIENT_ID,
                callback: handleGoogleLogin,
                auto_select: false,
            });
            const btnContainer = document.getElementById('googleSignInBtn');
            if (btnContainer) {
                btnContainer.innerHTML = '';
                google.accounts.id.renderButton(btnContainer, {
                    theme: 'filled_blue', size: 'large', width: 280,
                    text: 'signin_with', shape: 'rectangular',
                });
            }
        } catch(e) {}
    }
}

function closeLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}

function handleGoogleLogin(response) {
    try {
        const parts = response.credential.split('.');
        const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));
        const user = {
            name: payload.name || 'Pengguna Google',
            email: payload.email || '',
            picture: payload.picture || '',
            sub: payload.sub || '',
        };
        localStorage.setItem('auspotyGoogleUser', JSON.stringify(user));
        closeLoginModal();
        updateProfileUI();
        showToast('Selamat datang, ' + user.name.split(' ')[0] + '!');
    } catch(e) {
        showToast('Login gagal, coba lagi');
    }
}

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
    print('Login block replaced OK')
else:
    marker = '// ===================== GOOGLE LOGIN ====================='
    init_marker = '\n// INIT'
    start = js.find(marker)
    end = js.find(init_marker)
    if start != -1 and end != -1:
        js = js[:start] + new_block.strip() + '\n' + js[end:]
        print('Login block replaced via manual find OK')
    else:
        print('ERROR: markers not found')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print('script.js saved OK')
