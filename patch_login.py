import re

# ============================================================
# PATCH index.html — tambah Google GSI script + login modal
# ============================================================
html_path = r'C:\Users\Admin\Downloads\Auspoty\public\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Tambah Google GSI script di <head>
gsi_script = '    <script src="https://accounts.google.com/gsi/client" async defer></script>\n'
html = html.replace(
    '    <script src="https://www.youtube.com/iframe_api"></script>\n',
    '    <script src="https://www.youtube.com/iframe_api"></script>\n' + gsi_script
)

# 2. Ganti settings profile card — tambah tombol login Google
old_profile = '''    <!-- Profil -->
    <div class="settings-profile-card" onclick="openEditProfile()">
        <div class="settings-avatar" id="settingsAvatar">A</div>
        <div class="settings-profile-info">
            <div class="settings-profile-name" id="settingsProfileName">Pengguna Auspoty</div>
            <div class="settings-profile-sub">Auspoty Premium</div>
        </div>
        <svg viewBox="0 0 24 24" style="fill:var(--text-sub);width:20px;height:20px;flex-shrink:0;"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z"/></svg>
    </div>'''

new_profile = '''    <!-- Profil -->
    <div class="settings-profile-card" id="profileCard" onclick="openEditProfile()">
        <div class="settings-avatar" id="settingsAvatar">A</div>
        <div class="settings-profile-info">
            <div class="settings-profile-name" id="settingsProfileName">Pengguna Auspoty</div>
            <div class="settings-profile-sub" id="settingsProfileSub">Auspoty Premium</div>
        </div>
        <svg viewBox="0 0 24 24" style="fill:var(--text-sub);width:20px;height:20px;flex-shrink:0;"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z"/></svg>
    </div>
    <!-- Tombol Login/Logout Google -->
    <div id="googleLoginBtn" class="settings-group" style="margin-bottom:0;cursor:pointer;" onclick="loginWithGoogle()">
        <div class="settings-item">
            <div class="settings-item-left">
                <div class="settings-icon" style="background:#fff;padding:6px;">
                    <svg viewBox="0 0 48 48" style="width:24px;height:24px;"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/><path fill="none" d="M0 0h48v48H0z"/></svg>
                </div>
                <div><div class="settings-item-title" id="googleLoginText">Masuk dengan Google</div><div class="settings-item-sub" id="googleLoginSub">Sinkronkan data kamu</div></div>
            </div>
            <svg viewBox="0 0 24 24" class="settings-chevron"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z"/></svg>
        </div>
    </div>'''

html = html.replace(old_profile, new_profile)

# 3. Tambah login modal sebelum </body>
login_modal = '''
<!-- GOOGLE LOGIN MODAL -->
<div id="loginModal" style="display:none;position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,0.85);display:none;align-items:center;justify-content:center;">
    <div style="background:#1a1a2e;border-radius:16px;padding:32px 24px;width:90%;max-width:360px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.8);">
        <div style="font-size:40px;margin-bottom:12px;">🎵</div>
        <h2 style="color:white;font-size:22px;font-weight:700;margin-bottom:8px;">Masuk ke Auspoty</h2>
        <p style="color:rgba(255,255,255,0.6);font-size:14px;margin-bottom:28px;">Login untuk menyimpan playlist dan lagu favorit kamu</p>
        <!-- Google One Tap container -->
        <div id="g_id_onload"
             data-client_id="YOUR_GOOGLE_CLIENT_ID"
             data-callback="handleGoogleLogin"
             data-auto_prompt="false">
        </div>
        <div class="g_id_signin"
             data-type="standard"
             data-size="large"
             data-theme="outline"
             data-text="signin_with"
             data-shape="rectangular"
             data-logo_alignment="left"
             data-width="280">
        </div>
        <div style="margin-top:16px;">
            <button onclick="closeLoginModal()" style="background:transparent;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.6);padding:10px 24px;border-radius:20px;font-size:14px;cursor:pointer;">Nanti saja</button>
        </div>
    </div>
</div>

'''

html = html.replace('</body>', login_modal + '</body>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML patched OK')

# ============================================================
# PATCH script.js — tambah fungsi login Google
# ============================================================
js_path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

login_js = '''
// ===================== GOOGLE LOGIN =====================
function loginWithGoogle() {
    const user = getGoogleUser();
    if (user) {
        // Sudah login — tanya mau logout
        if (confirm('Keluar dari akun ' + user.name + '?')) {
            localStorage.removeItem('auspotyGoogleUser');
            updateProfileUI();
            showToast('Berhasil keluar');
        }
        return;
    }
    // Belum login — tampilkan modal
    document.getElementById('loginModal').style.display = 'flex';
    // Render Google button
    if (window.google && window.google.accounts) {
        google.accounts.id.initialize({
            client_id: '438992596571-example.apps.googleusercontent.com',
            callback: handleGoogleLogin,
            auto_select: false,
        });
        google.accounts.id.renderButton(
            document.querySelector('.g_id_signin'),
            { theme: 'outline', size: 'large', width: 280 }
        );
    }
}
function closeLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}
function handleGoogleLogin(response) {
    try {
        // Decode JWT payload
        const payload = JSON.parse(atob(response.credential.split('.')[1]));
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
        // Update avatar
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
        // Update home avatar
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
'''

# Tambah sebelum // ===================== INIT =====================
js = js.replace('// INIT\napplyAllSettings();', login_js + '\n// INIT\napplyAllSettings();')

# Panggil updateProfileUI() di INIT
js = js.replace(
    '// INIT\napplyAllSettings();\nloadHomeData();\nrenderSearchCategories();',
    '// INIT\napplyAllSettings();\nupdateProfileUI();\nloadHomeData();\nrenderSearchCategories();'
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print('JS patched OK')
