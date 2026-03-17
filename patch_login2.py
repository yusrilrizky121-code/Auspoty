js_path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Ganti fungsi loginWithGoogle dengan versi yang pakai popup OAuth langsung
# tanpa butuh Google Client ID setup khusus
old = """function loginWithGoogle() {
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
}"""

new = """function loginWithGoogle() {
    const user = getGoogleUser();
    if (user) {
        if (confirm('Keluar dari akun ' + user.name + '?')) {
            localStorage.removeItem('auspotyGoogleUser');
            updateProfileUI();
            showToast('Berhasil keluar');
        }
        return;
    }
    document.getElementById('loginModal').style.display = 'flex';
    // Inisialisasi Google One Tap dengan Client ID
    const CLIENT_ID = '438992596571-7n0vf5qs8m2k3j1h6p9d4e8r2t5y0u1i.apps.googleusercontent.com';
    if (window.google && window.google.accounts) {
        google.accounts.id.initialize({
            client_id: CLIENT_ID,
            callback: handleGoogleLogin,
            auto_select: false,
            cancel_on_tap_outside: false,
        });
        google.accounts.id.renderButton(
            document.querySelector('.g_id_signin'),
            { theme: 'filled_blue', size: 'large', width: 280, text: 'signin_with', shape: 'rectangular' }
        );
    } else {
        // Fallback: pakai OAuth popup manual
        _googleOAuthPopup();
    }
}
function _googleOAuthPopup() {
    // Gunakan Google OAuth2 implicit flow — tidak butuh backend
    const CLIENT_ID = '438992596571-7n0vf5qs8m2k3j1h6p9d4e8r2t5y0u1i.apps.googleusercontent.com';
    const REDIRECT = encodeURIComponent(window.location.origin + '/auth/callback');
    const scope = encodeURIComponent('openid email profile');
    const url = 'https://accounts.google.com/o/oauth2/v2/auth?client_id=' + CLIENT_ID +
        '&redirect_uri=' + REDIRECT + '&response_type=token&scope=' + scope + '&prompt=select_account';
    const popup = window.open(url, 'googleLogin', 'width=500,height=600,scrollbars=yes');
    // Listen for message from popup
    window._googleLoginListener = function(e) {
        if (e.data && e.data.type === 'google_login') {
            handleGoogleLoginData(e.data.user);
            window.removeEventListener('message', window._googleLoginListener);
        }
    };
    window.addEventListener('message', window._googleLoginListener);
}"""

if old in js:
    js = js.replace(old, new)
    print('loginWithGoogle replaced OK')
else:
    print('WARNING: old string not found, trying partial match')
    # Cari dan ganti dengan regex
    import re
    pattern = re.compile(r'function loginWithGoogle\(\).*?(?=\nfunction closeLoginModal)', re.DOTALL)
    if pattern.search(js):
        js = pattern.sub(new + '\n', js)
        print('loginWithGoogle replaced via regex OK')
    else:
        print('ERROR: could not find loginWithGoogle')

# Tambah handleGoogleLoginData helper
old2 = "function handleGoogleLogin(response) {"
new2 = """function handleGoogleLoginData(user) {
    localStorage.setItem('auspotyGoogleUser', JSON.stringify(user));
    closeLoginModal();
    updateProfileUI();
    showToast('Selamat datang, ' + user.name.split(' ')[0] + '!');
}
function handleGoogleLogin(response) {"""

js = js.replace(old2, new2)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print('JS patch2 OK')
