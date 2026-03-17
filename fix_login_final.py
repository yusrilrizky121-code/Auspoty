import re

# ============================================================
# FIX LOGIN GOOGLE — implementasi lengkap yang bisa jalan
# ============================================================

js_path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
html_path = r'C:\Users\Admin\Downloads\Auspoty\public\index.html'

# ---- PATCH script.js ----
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Hapus seluruh blok GOOGLE LOGIN lama dan ganti dengan yang baru
old_block = re.compile(
    r'// ===================== GOOGLE LOGIN =====================.*?(?=\n// INIT)',
    re.DOTALL
)

new_login_block = r"""// ===================== GOOGLE LOGIN =====================
// Ganti CLIENT_ID di bawah dengan Client ID dari Google Cloud Console
// Cara buat: https://console.cloud.google.com → APIs & Services → Credentials → Create OAuth 2.0 Client ID
// Authorized JS origins: https://clone2-iyrr-git-master-yusrilrizky121-codes-projects.vercel.app
const GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'; // <-- GANTI INI

function loginWithGoogle() {
    const user = getGoogleUser();
    if (user) {
        if (confirm('Keluar dari akun ' + user.name + '?')) {
            localStorage.removeItem('auspotyGoogleUser');
            updateProfileUI();
            showToast('Berhasil keluar');
        }
        return;
    }
    _showLoginModal();
}

function _showLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.style.display = 'flex';
    // Coba render Google button jika GSI sudah load dan Client ID valid
    if (window.google && window.google.accounts && GOOGLE_CLIENT_ID !== 'YOUR_GOOGLE_CLIENT_ID') {
        try {
            google.accounts.id.initialize({
                client_id: GOOGLE_CLIENT_ID,
                callback: handleGoogleLogin,
                auto_select: false,
                cancel_on_tap_outside: false,
            });
            const btnContainer = document.getElementById('googleSignInBtn');
            if (btnContainer) {
                btnContainer.innerHTML = '';
                google.accounts.id.renderButton(btnContainer, {
                    theme: 'filled_blue',
                    size: 'large',
                    width: 280,
                    text: 'signin_with',
                    shape: 'rectangular',
                    logo_alignment: 'left',
                });
            }
        } catch(e) {
            console.error('Google GSI error:', e);
        }
    }
}

function closeLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}

function handleGoogleLogin(response) {
    try {
        // Decode JWT payload (base64url decode)
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
        console.error('Login error:', e);
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
    js = old_block.sub(new_login_block.strip(), js)
    print('Login block replaced OK')
else:
    print('ERROR: login block not found via regex')
    # Coba cari manual
    marker = '// ===================== GOOGLE LOGIN ====================='
    init_marker = '\n// INIT'
    start = js.find(marker)
    end = js.find(init_marker)
    if start != -1 and end != -1:
        js = js[:start] + new_login_block.strip() + '\n' + js[end:]
        print('Login block replaced via manual find OK')
    else:
        print('ERROR: markers not found, start=%d end=%d' % (start, end))

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print('script.js saved OK')

# ---- PATCH index.html — ganti loginModal ----
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Ganti seluruh loginModal dengan versi baru yang lebih bagus
old_modal = re.compile(
    r'<!-- GOOGLE LOGIN MODAL -->.*?</div>\s*\n\s*</body>',
    re.DOTALL
)

new_modal = """<!-- GOOGLE LOGIN MODAL -->
<div id="loginModal" style="display:none;position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,0.9);align-items:center;justify-content:center;">
    <div style="background:#1a1a2e;border-radius:20px;padding:32px 24px 28px;width:90%;max-width:360px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.8);position:relative;">
        <button onclick="closeLoginModal()" style="position:absolute;top:14px;right:14px;background:rgba(255,255,255,0.1);border:none;color:white;width:30px;height:30px;border-radius:50%;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;">✕</button>
        <div style="font-size:44px;margin-bottom:10px;">🎵</div>
        <h2 style="color:white;font-size:22px;font-weight:700;margin-bottom:6px;">Masuk ke Auspoty</h2>
        <p style="color:rgba(255,255,255,0.55);font-size:13px;margin-bottom:24px;line-height:1.5;">Login untuk menyimpan playlist<br>dan lagu favorit kamu</p>
        <!-- Google Sign-In Button container -->
        <div id="googleSignInBtn" style="display:flex;justify-content:center;min-height:44px;margin-bottom:12px;"></div>
        <!-- Fallback jika Client ID belum diset -->
        <div id="loginSetupInfo" style="display:none;background:rgba(255,255,255,0.05);border-radius:12px;padding:16px;text-align:left;margin-bottom:16px;">
            <p style="color:#ffd700;font-size:12px;font-weight:700;margin-bottom:8px;">⚙️ Setup diperlukan</p>
            <p style="color:rgba(255,255,255,0.6);font-size:11px;line-height:1.6;margin-bottom:8px;">Untuk mengaktifkan login Google, buat Client ID di Google Cloud Console lalu ganti <code style="color:#1ed760;">GOOGLE_CLIENT_ID</code> di script.js</p>
            <a href="https://console.cloud.google.com/apis/credentials" target="_blank" style="color:#1ed760;font-size:11px;text-decoration:none;">→ Buka Google Cloud Console</a>
        </div>
        <button onclick="closeLoginModal()" style="background:transparent;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.5);padding:10px 28px;border-radius:20px;font-size:13px;cursor:pointer;width:100%;">Nanti saja</button>
    </div>
</div>

<script>
// Tampilkan info setup jika Client ID belum diset
document.addEventListener('DOMContentLoaded', function() {
    // Cek apakah Google GSI sudah load
    function checkGoogleReady() {
        const info = document.getElementById('loginSetupInfo');
        const btnContainer = document.getElementById('googleSignInBtn');
        if (typeof GOOGLE_CLIENT_ID !== 'undefined' && GOOGLE_CLIENT_ID === 'YOUR_GOOGLE_CLIENT_ID') {
            if (info) info.style.display = 'block';
            if (btnContainer) btnContainer.innerHTML = '<div style="color:rgba(255,255,255,0.3);font-size:12px;padding:10px;">Google Sign-In belum dikonfigurasi</div>';
        }
    }
    setTimeout(checkGoogleReady, 500);
});
</script>

</body>
</html>"""

if old_modal.search(html):
    html = old_modal.sub(new_modal, html)
    print('loginModal replaced OK')
else:
    # Coba cari manual
    marker = '<!-- GOOGLE LOGIN MODAL -->'
    end_marker = '</body>\n</html>'
    start = html.find(marker)
    end = html.rfind('</body>')
    if start != -1 and end != -1:
        html = html[:start] + new_modal
        print('loginModal replaced via manual find OK')
    else:
        print('ERROR: loginModal not found')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html saved OK')
print('\nDone! Login Google siap. Untuk mengaktifkan:')
print('1. Buka https://console.cloud.google.com')
print('2. Buat OAuth 2.0 Client ID (Web application)')
print('3. Tambah authorized origin: https://clone2-iyrr-git-master-yusrilrizky121-codes-projects.vercel.app')
print('4. Ganti GOOGLE_CLIENT_ID di public/script.js')
