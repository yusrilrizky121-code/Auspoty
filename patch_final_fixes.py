import re

with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix openEditProfile - tambah prioritas foto Google
old_profile = """    const av = document.getElementById('editProfileAvatar');
    const savedPhoto = localStorage.getItem('auspotyProfilePhoto');
    if (savedPhoto) {
        av.innerHTML = '<img src="' + savedPhoto + '" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
    } else {
        av.innerText = (s.profileName || 'A').charAt(0).toUpperCase();
    }
    document.getElementById('editProfileModal').style.display = 'flex';
}
function triggerPhotoUpload() { document.getElementById('profilePhotoInput').click(); }
function handleProfilePhotoChange(event) {"""

new_profile = """    const av = document.getElementById('editProfileAvatar');
    const user = getGoogleUser();
    // Prioritas: foto Google > foto upload lokal > inisial
    if (user && user.picture) {
        av.innerHTML = '<img src="' + user.picture + '" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
        document.getElementById('editProfileName').value = user.name;
    } else {
        const savedPhoto = localStorage.getItem('auspotyProfilePhoto');
        if (savedPhoto) {
            av.innerHTML = '<img src="' + savedPhoto + '" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">';
        } else {
            av.innerText = (s.profileName || 'A').charAt(0).toUpperCase();
        }
    }
    document.getElementById('editProfileModal').style.display = 'flex';
}
function triggerPhotoUpload() { document.getElementById('profilePhotoInput').click(); }
function previewProfilePhoto(event) { handleProfilePhotoChange(event); }
function handleProfilePhotoChange(event) {"""

if old_profile in content:
    content = content.replace(old_profile, new_profile)
    print("OK: openEditProfile fixed")
else:
    print("WARN: openEditProfile pattern not found, trying byte-level search...")
    # Try with different quotes
    with open('public/script.js', 'rb') as f:
        raw = f.read()
    snippet = raw[raw.find(b'editProfileAvatar'):raw.find(b'editProfileAvatar')+600]
    print(repr(snippet))

# 2. Fix loadComments - tambah tombol hapus untuk admin
old_comments = """        const docs = snap.docs.map(doc => doc.data());
        docs.sort((a, b) => (b.createdAt ? b.createdAt.seconds : 0) - (a.createdAt ? a.createdAt.seconds : 0));
        list.innerHTML = docs.map(d => {
            const isAdmin = d.email === 'yusrilrizky149@gmail.com';
            const badge = isAdmin
                ? '<span style="background:linear-gradient(135deg,#a78bfa,#f472b6);color:#fff;font-size:10px;font-weight:700;padding:2px 8px;border-radius:10px;margin-left:6px;">ADMIN</span>'
                : '<span style="background:rgba(255,255,255,0.1);color:var(--text-sub);font-size:10px;font-weight:600;padding:2px 8px;border-radius:10px;margin-left:6px;">Pengguna</span>';
            const time = d.createdAt ? new Date(d.createdAt.seconds * 1000).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '';
            return '<div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:12px;">' +
                '<div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:#fff;flex-shrink:0;overflow:hidden;">' + (d.picture ? '<img src="' + d.picture + '" style="width:100%;height:100%;object-fit:cover;">' : d.name.charAt(0).toUpperCase()) + '</div>' +
                '<div style="flex:1;background:rgba(255,255,255,0.06);border-radius:12px;padding:10px 14px;">' +
                '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;flex-wrap:wrap;gap:4px;"><span style="font-size:13px;font-weight:700;color:var(--accent);">' + d.name + badge + '</span><span style="font-size:11px;color:var(--text-sub);">' + time + '</span></div>' +
                '<p style="font-size:14px;color:white;line-height:1.5;margin:0;">' + d.text + '</p></div></div>';
        }).join('');"""

new_comments = """        const docs = snap.docs.map((doc) => ({ id: doc.id, ...doc.data() }));
        docs.sort((a, b) => (b.createdAt ? b.createdAt.seconds : 0) - (a.createdAt ? a.createdAt.seconds : 0));
        const currentUser = getGoogleUser();
        const isCurrentAdmin = currentUser && currentUser.email === 'yusrilrizky149@gmail.com';
        list.innerHTML = docs.map(d => {
            const isAdmin = d.email === 'yusrilrizky149@gmail.com';
            const badge = isAdmin
                ? '<span style="background:linear-gradient(135deg,#a78bfa,#f472b6);color:#fff;font-size:10px;font-weight:700;padding:2px 8px;border-radius:10px;margin-left:6px;">ADMIN</span>'
                : '<span style="background:rgba(255,255,255,0.1);color:var(--text-sub);font-size:10px;font-weight:600;padding:2px 8px;border-radius:10px;margin-left:6px;">Pengguna</span>';
            const time = d.createdAt ? new Date(d.createdAt.seconds * 1000).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '';
            const deleteBtn = isCurrentAdmin
                ? '<button onclick="deleteComment(\\'' + d.id + '\\',\\'' + videoId + '\\')" style="background:rgba(255,82,82,0.15);border:none;color:#ff5252;font-size:11px;padding:3px 10px;border-radius:8px;cursor:pointer;margin-left:8px;">Hapus</button>'
                : '';
            return '<div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:12px;">' +
                '<div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:#fff;flex-shrink:0;overflow:hidden;">' + (d.picture ? '<img src="' + d.picture + '" style="width:100%;height:100%;object-fit:cover;">' : d.name.charAt(0).toUpperCase()) + '</div>' +
                '<div style="flex:1;background:rgba(255,255,255,0.06);border-radius:12px;padding:10px 14px;">' +
                '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;flex-wrap:wrap;gap:4px;"><span style="font-size:13px;font-weight:700;color:var(--accent);">' + d.name + badge + deleteBtn + '</span><span style="font-size:11px;color:var(--text-sub);">' + time + '</span></div>' +
                '<p style="font-size:14px;color:white;line-height:1.5;margin:0;">' + d.text + '</p></div></div>';
        }).join('');"""

if old_comments in content:
    content = content.replace(old_comments, new_comments)
    print("OK: loadComments fixed with delete button")
else:
    print("WARN: loadComments pattern not found")

# 3. Tambah fungsi deleteComment dan openHistoryView sebelum // INIT
old_init = """// INIT
applyAllSettings();
updateProfileUI();
loadHomeData();
renderSearchCategories();"""

new_init = """// DELETE COMMENT (admin only)
async function deleteComment(docId, videoId) {
    const user = getGoogleUser();
    if (!user || user.email !== 'yusrilrizky149@gmail.com') { showToast('Hanya admin yang bisa menghapus'); return; }
    if (!confirm('Hapus komentar ini?')) return;
    try {
        const { getFirestore, doc, deleteDoc } = await import('https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js');
        const db_fs = window._firestoreDB;
        const { doc: fsDoc, deleteDoc: fsDelete } = { doc: window._fsDoc, deleteDoc: window._fsDelete };
        // Gunakan deleteDoc dari Firestore
        const colRef = window._fsCollection(db_fs, 'comments');
        const snap2 = await window._fsGetDocs(window._fsQuery(colRef, window._fsWhere('__name__', '==', docId)));
        // Fallback: cari by id manual
        const allSnap = await window._fsGetDocs(window._fsQuery(colRef, window._fsWhere('videoId', '==', videoId)));
        const target = allSnap.docs.find(d => d.id === docId);
        if (target) {
            await target.ref.delete();
            showToast('Komentar dihapus');
            loadComments(videoId);
        } else { showToast('Komentar tidak ditemukan'); }
    } catch(e) { showToast('Gagal hapus: ' + e.message); }
}

// HISTORY VIEW
function openHistoryView() {
    const history = JSON.parse(localStorage.getItem('auspotyHistory') || '[]');
    const container = document.getElementById('libraryContainer');
    if (!container) return;
    const backBtn = '<div style="padding:0 16px 8px;"><button onclick="renderLibraryUI()" style="background:rgba(255,255,255,0.1);border:none;color:white;padding:8px 16px;border-radius:20px;font-size:13px;cursor:pointer;">\u2190 Kembali ke Koleksi</button></div>';
    if (history.length === 0) {
        container.innerHTML = backBtn + '<div style="color:var(--text-sub);padding:20px;text-align:center;font-size:14px;">Belum ada riwayat putar.</div>';
        return;
    }
    container.innerHTML = backBtn + history.slice(0, 30).map(t => renderVItem(t)).join('');
}

// INIT
applyAllSettings();
updateProfileUI();
loadHomeData();
renderSearchCategories();"""

if old_init in content:
    content = content.replace(old_init, new_init)
    print("OK: deleteComment + openHistoryView added")
else:
    print("WARN: INIT pattern not found")

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
