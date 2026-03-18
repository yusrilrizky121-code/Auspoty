with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fungsi yang perlu ditambahkan sebelum // GOOGLE USER HELPER
login_funcs = '''// LOGIN / LOGOUT GOOGLE
function loginWithGoogle() {
    if (typeof window._firebaseSignIn === 'function') {
        window._firebaseSignIn();
    } else {
        showToast('Firebase belum siap, coba lagi');
    }
}

function logoutFromGoogle() {
    if (typeof window._firebaseSignOut === 'function') {
        window._firebaseSignOut().then(() => {
            updateGoogleLoginUI();
        });
    } else {
        localStorage.removeItem('auspotyGoogleUser');
        updateGoogleLoginUI();
        showToast('Berhasil keluar');
    }
}

function updateGoogleLoginUI() {
    var user = getGoogleUser();
    var loginBtn  = document.getElementById('googleLoginBtn');
    var logoutBtn = document.getElementById('googleLogoutBtn');
    var loginText = document.getElementById('googleLoginText');
    var loginSub  = document.getElementById('googleLoginSub');
    var logoutSub = document.getElementById('googleLogoutSub');
    if (user) {
        if (loginBtn)  loginBtn.style.display  = 'none';
        if (logoutBtn) logoutBtn.style.display = '';
        if (logoutSub) logoutSub.innerText = user.name || 'Tap untuk logout';
    } else {
        if (loginBtn)  loginBtn.style.display  = '';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (loginSub)  loginSub.innerText = 'Sinkronkan data kamu';
    }
    updateProfileUI();
}

'''

marker = '// GOOGLE USER HELPER'
if 'function loginWithGoogle' in content:
    print('loginWithGoogle already exists')
else:
    if marker in content:
        content = content.replace(marker, login_funcs + marker)
        print('PATCHED: login funcs added')
    else:
        # fallback: prepend before // INIT
        content = content.replace('// INIT\n', login_funcs + '// INIT\n')
        print('PATCHED: login funcs added before INIT')

# Also patch updateProfileUI to call updateGoogleLoginUI at the end
if 'updateGoogleLoginUI' not in content:
    print('WARNING: updateGoogleLoginUI not injected properly')

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)

# Also patch INIT to call updateGoogleLoginUI after updateProfileUI
with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_init = '// INIT\napplyAllSettings();\nupdateProfileUI();\nloadHomeData();\nrenderSearchCategories();'
new_init = '// INIT\napplyAllSettings();\nupdateProfileUI();\nupdateGoogleLoginUI();\nloadHomeData();\nrenderSearchCategories();'

if 'updateGoogleLoginUI();' not in content:
    if old_init in content:
        content = content.replace(old_init, new_init)
        print('PATCHED: updateGoogleLoginUI added to INIT')
    else:
        print('WARNING: INIT block not found for patching')
    with open('public/script.js', 'w', encoding='utf-8') as f:
        f.write(content)

print('DONE')
