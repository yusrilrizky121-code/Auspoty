with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Fix openEditProfile - sudah bagus, hanya perlu pastikan
#    foto Google muncul saat ganti akun (sudah ada customPhoto logic)
#    Tambahkan: jika user Google ada, prioritaskan foto Google
# ============================================================
old1 = """    var customPhoto = localStorage.getItem('auspotyCustomPhoto');
    if (av) {
        var photoSrc = customPhoto || (user ? user.picture : null);"""

new1 = """    var customPhoto = localStorage.getItem('auspotyCustomPhoto');
    if (av) {
        // Saat ganti akun Google, hapus foto custom lama agar foto Google tampil
        var photoSrc = (user && user.picture && !customPhoto) ? user.picture : (customPhoto || (user ? user.picture : null));"""

if old1 in content:
    content = content.replace(old1, new1)
    print("OK: openEditProfile photo priority fixed")
else:
    print("WARN: old1 not found")

# ============================================================
# 2. Fix loadComments - tambah doc.id dan tombol hapus admin
# ============================================================
old2 = "        const docs = snap.docs.map(d=>d.data()).sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));"
new2 = "        const docs = snap.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));\n        const currentUser = getGoogleUser();\n        const isCurrentAdmin = currentUser && currentUser.email === 'yusrilrizky149@gmail.com';"

if old2 in content:
    content = content.replace(old2, new2)
    print("OK: loadComments docs mapping fixed")
else:
    print("WARN: old2 not found, trying alternate...")
    # Try with different whitespace
    import re
    m = re.search(r'const docs = snap\.docs\.map\(d=>d\.data\(\)\)\.sort', content)
    if m:
        print("Found at:", m.start())
        print(repr(content[m.start():m.start()+100]))
    else:
        print("Not found at all")

# 3. Tambah delete button di render komentar
old3 = """            const isAdmin = d.email === 'yusrilrizky149@gmail.com';
            const badge = isAdmin ? '<span style="background:linear-gradient(135deg,#f59e0b,#ef4444);color:#fff;font-size:10px;font-weight:800;padding:2px 7px;border-radius:8px;margin-left:6px;letter-spacing:.5px;">ADMIN</span>' : '<span style="background:rgba(255,255,255,0.1);color:var(--text-sub);font-size:10p"""

# Cari pola yang ada
i = content.find("const isAdmin = d.email === 'yusrilrizky149@gmail.com'")
if i >= 0:
    print("Found isAdmin at:", i)
    print(repr(content[i:i+600]))
else:
    print("isAdmin not found")

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")
