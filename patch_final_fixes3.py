with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Tambah delete button di render komentar
# ============================================================
old_badge_block = """            const isAdmin = d.email === 'yusrilrizky149@gmail.com';
            const badge = isAdmin ? '<span style="background:linear-gradient(135deg,#f59e0b,#ef4444);color:#fff;font-size:10px;font-weight:800;padding:2px 7px;border-radius:8px;margin-left:6px;letter-spacing:.5px;">ADMIN</span>' : '<span style="background:rgba(255,255,255,0.1);color:var(--text-sub);font-size:10px;font-weight:600;padding:2px 7px;border-radius:8px;margin-left:6px;">Pengguna</span>';
            return '<div style="display:flex;gap:10px;align-items:flex-start;">"""

new_badge_block = """            const isAdmin = d.email === 'yusrilrizky149@gmail.com';
            const badge = isAdmin ? '<span style="background:linear-gradient(135deg,#f59e0b,#ef4444);color:#fff;font-size:10px;font-weight:800;padding:2px 7px;border-radius:8px;margin-left:6px;letter-spacing:.5px;">ADMIN</span>' : '<span style="background:rgba(255,255,255,0.1);color:var(--text-sub);font-size:10px;font-weight:600;padding:2px 7px;border-radius:8px;margin-left:6px;">Pengguna</span>';
            const deleteBtn = isCurrentAdmin ? '<button onclick="deleteComment(\\'' + d.id + '\\',\\'' + videoId + '\\')" style="background:rgba(255,82,82,0.15);border:none;color:#ff5252;font-size:11px;padding:3px 8px;border-radius:6px;cursor:pointer;margin-left:6px;">Hapus</button>' : '';
            return '<div style="display:flex;gap:10px;align-items:flex-start;">"""

if old_badge_block in content:
    content = content.replace(old_badge_block, new_badge_block)
    print("OK: delete button added to comment render")
else:
    print("WARN: badge block not found, searching...")
    i = content.find("const isAdmin = d.email")
    print(repr(content[i:i+300]))

# ============================================================
# 2. Tambah deleteBtn ke HTML komentar
# ============================================================
# Cari bagian nama + badge di return HTML
old_name_line = """'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;"><span style="font-size:13px;font-weight:700;color:var(--accent);">' + d.name + badge + '</span>"""

new_name_line = """'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;"><span style="font-size:13px;font-weight:700;color:var(--accent);">' + d.name + badge + deleteBtn + '</span>"""

if old_name_line in content:
    content = content.replace(old_name_line, new_name_line)
    print("OK: deleteBtn injected into comment HTML")
else:
    # Cari pola yang ada
    i = content.find("d.name + badge")
    if i >= 0:
        print("Found d.name + badge at:", i)
        print(repr(content[i:i+200]))
    else:
        print("WARN: d.name + badge not found")

# ============================================================
# 3. Tambah fungsi deleteComment dan openHistoryView sebelum // INIT
# ============================================================
old_init = "// INIT\napplyAllSettings();\nloadHomeData();\nrenderSearchCategories();"

new_init = """// DELETE COMMENT (admin only)
async function deleteComment(docId, videoId) {
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
loadHomeData();
renderSearchCategories();"""

if old_init in content:
    content = content.replace(old_init, new_init)
    print("OK: deleteComment + openHistoryView added")
else:
    print("WARN: INIT not found")
    i = content.find('// INIT')
    print(repr(content[i:i+100]))

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
