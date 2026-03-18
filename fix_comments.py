js_path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
with open(js_path, encoding='utf-8') as f:
    js = f.read()

# Hapus orderBy dari query
js = js.replace(
    "window._fsWhere('videoId','==',videoId),window._fsOrderBy('createdAt','desc')",
    "window._fsWhere('videoId','==',videoId)"
)

# Sort di client setelah getDocs
old = "const snap = await window._fsGetDocs(q);\n        if (snap.empty) { list.innerHTML = '<div style=\"color:var(--text-sub);text-align:center;padding:20px;font-size:13px;\">Belum ada komentar. Jadilah yang pertama!</div>'; return; }\n        list.innerHTML = snap.docs.map(doc => {\n            const d = doc.data();"
new = "const snap = await window._fsGetDocs(q);\n        if (snap.empty) { list.innerHTML = '<div style=\"color:var(--text-sub);text-align:center;padding:20px;font-size:13px;\">Belum ada komentar. Jadilah yang pertama!</div>'; return; }\n        const docs = snap.docs.map(d=>d.data()).sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));\n        list.innerHTML = docs.map(d => {"

if old in js:
    js = js.replace(old, new)
    print("replaced snap.docs section")
else:
    # Coba cari versi lain
    idx = js.find("snap.docs.map(doc =>")
    print("snap.docs.map found at:", idx)
    print("Context:", repr(js[max(0,idx-50):idx+100]))

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("done")
