with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Fix deleteComment — pakai window._fsDeleteDoc + window._fsDoc
# ============================================================
old_delete = """async function deleteComment(docId, videoId) {
    const user = getGoogleUser();
    if (!user || user.email !== 'yusrilrizky149@gmail.com') { showToast('Hanya admin yang bisa menghapus'); return; }
    if (!confirm('Hapus komentar ini?')) return;
    try {
        const db_fs = window._firestoreDB;
        const allSnap = await window._fsGetDocs(window._fsQuery(window._fsCollection(db_fs, 'comments'), window._fsWhere('videoId', '==', videoId)));
        const target = allSnap.docs.find(d => d.id === docId);
        if (target) {
            await target.ref.delete();
            showToast('Komentar dihapus');
            loadComments(videoId);
        } else { showToast('Komentar tidak ditemukan'); }
    } catch(e) { showToast('Gagal hapus: ' + e.message); }
}"""

new_delete = """async function deleteComment(docId, videoId) {
    const user = getGoogleUser();
    if (!user || user.email !== 'yusrilrizky149@gmail.com') { showToast('Hanya admin yang bisa menghapus'); return; }
    if (!confirm('Hapus komentar ini?')) return;
    try {
        const db_fs = window._firestoreDB;
        if (!db_fs || !window._fsDeleteDoc || !window._fsDoc) {
            showToast('Firestore belum siap, coba lagi'); return;
        }
        // Firestore v9 modular: deleteDoc(doc(db, collection, id))
        const docRef = window._fsDoc(db_fs, 'comments', docId);
        await window._fsDeleteDoc(docRef);
        showToast('Komentar dihapus');
        loadComments(videoId);
    } catch(e) { showToast('Gagal hapus: ' + e.message); }
}"""

if old_delete in content:
    content = content.replace(old_delete, new_delete)
    print("OK: deleteComment fixed")
else:
    print("WARN: deleteComment pattern not found, searching...")
    i = content.find('async function deleteComment')
    print(repr(content[i:i+600]))

# ============================================================
# 2. Fix previewProfilePhoto — pastikan update semua avatar
# ============================================================
old_preview = """function previewProfilePhoto(event) {
    var file = event.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function(e) {
        var dataUrl = e.target.result;
        localStorage.setItem('auspotyCustomPhoto', dataUrl);
        var av = document.getElementById("""

# Cari fungsi lengkap
i = content.find('function previewProfilePhoto')
end = content.find('\n}\n', i)
old_full = content[i:end+3]
print("\n=== previewProfilePhoto current ===")
print(repr(old_full))

new_preview = """function previewProfilePhoto(event) {
    var file = event.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function(e) {
        var dataUrl = e.target.result;
        localStorage.setItem('auspotyCustomPhoto', dataUrl);
        var imgTag = '<img src="' + dataUrl + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">';
        // Update avatar di modal edit profil
        var editAv = document.getElementById('editProfileAvatar');
        if (editAv) editAv.innerHTML = imgTag;
        // Update avatar di settings
        var settAv = document.getElementById('settingsAvatar');
        if (settAv) settAv.innerHTML = imgTag;
        // Update avatar di home header
        var homeAv = document.querySelector('.app-avatar');
        if (homeAv) homeAv.innerHTML = imgTag;
        showToast('Foto profil diperbarui!');
    };
    reader.readAsDataURL(file);
}
"""

if old_full:
    content = content.replace(old_full, new_preview)
    print("OK: previewProfilePhoto fixed")
else:
    print("WARN: previewProfilePhoto not replaced")

# ============================================================
# 3. Fix openEditProfile — pastikan foto custom SELALU tampil
#    bahkan saat user Google login (user bisa override foto Google)
# ============================================================
old_open = """function openEditProfile() {
    var s = getSettings();
    var user = getGoogleUser();
    var nameInput = document.getElementById('editProfileName');
    if (nameInput) nameInput.value = s.profileName || (user ? user.name : '');
    var av = document.getElementById('editProfileAvatar');
    var customPhoto = localStorage.getItem('auspotyCustomPhoto');
    if (av) {
        // Saat ganti akun Google, hapus foto custom lama agar foto Google tampil
        var photoSrc = (user && user.picture && !customPhoto) ? user.picture : (customPhoto || (user ? user.picture : null));
        if (photoSrc) {
            av.innerHTML = '<img src="' + photoSrc + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">';
        } else {
            av.innerHTML = '';
            av.innerText = (s.profileName || 'A').charAt(0).toUpperCase();
        }
    }"""

i2 = content.find('function openEditProfile')
end2 = content.find('\n}\n', i2)
old_open_full = content[i2:end2+3]
print("\n=== openEditProfile current ===")
print(repr(old_open_full[:300]))

new_open = """function openEditProfile() {
    var s = getSettings();
    var user = getGoogleUser();
    var nameInput = document.getElementById('editProfileName');
    if (nameInput) nameInput.value = user ? user.name : (s.profileName || '');
    var av = document.getElementById('editProfileAvatar');
    // Prioritas: foto custom upload > foto Google > inisial
    var customPhoto = localStorage.getItem('auspotyCustomPhoto');
    if (av) {
        if (customPhoto) {
            av.innerHTML = '<img src="' + customPhoto + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">';
        } else if (user && user.picture) {
            av.innerHTML = '<img src="' + user.picture + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">';
        } else {
            av.innerHTML = '';
            av.innerText = (user ? user.name : (s.profileName || 'A')).charAt(0).toUpperCase();
        }
    }
    var modal = document.getElementById('editProfileModal');
    if (modal) { modal.style.display = 'flex'; }
}
"""

if old_open_full:
    content = content.replace(old_open_full, new_open)
    print("OK: openEditProfile fixed")
else:
    print("WARN: openEditProfile not replaced")

# ============================================================
# 4. Fix updateProfileUI — tampilkan foto custom jika ada
#    (override foto Google dengan foto custom user)
# ============================================================
# Cari bagian saat user login Google — update avatar
old_google_av = """        const av = document.getElementById('settingsAvatar');
        if (av) { if (user.picture) { av.innerHTML = '<img src="'+user.picture+'" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">'; } else { av.innerText = user.name.charAt(0).toUpperCase(); } }"""

new_google_av = """        const av = document.getElementById('settingsAvatar');
        if (av) {
            const customPhoto = localStorage.getItem('auspotyCustomPhoto');
            if (customPhoto) {
                av.innerHTML = '<img src="'+customPhoto+'" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
            } else if (user.picture) {
                av.innerHTML = '<img src="'+user.picture+'" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
            } else {
                av.innerText = user.name.charAt(0).toUpperCase();
            }
        }"""

if old_google_av in content:
    content = content.replace(old_google_av, new_google_av)
    print("OK: updateProfileUI Google avatar fixed")
else:
    print("WARN: updateProfileUI Google avatar pattern not found")
    i3 = content.find("function updateProfileUI")
    print(repr(content[i3:i3+400]))

# Juga fix homeAv di updateProfileUI saat Google login
old_home_av = """        const homeAv = document.querySelector('.app-avatar');
        if (homeAv) { if (user.picture) { homeAv.innerHTML = '<img src="'+user.picture+'" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">'; } else { homeAv.innerText = user.name.charAt(0).toUpperCase(); } }"""

new_home_av = """        const homeAv = document.querySelector('.app-avatar');
        if (homeAv) {
            const customPhotoH = localStorage.getItem('auspotyCustomPhoto');
            if (customPhotoH) {
                homeAv.innerHTML = '<img src="'+customPhotoH+'" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
            } else if (user.picture) {
                homeAv.innerHTML = '<img src="'+user.picture+'" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
            } else {
                homeAv.innerText = user.name.charAt(0).toUpperCase();
            }
        }"""

if old_home_av in content:
    content = content.replace(old_home_av, new_home_av)
    print("OK: updateProfileUI homeAv fixed")
else:
    print("WARN: homeAv pattern not found")

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("\nDone!")
