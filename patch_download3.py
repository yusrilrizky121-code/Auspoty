src = open(r"C:\Users\Admin\Downloads\Auspoty\public\script.js", encoding="utf-8").read()

old = """        if (result.status === 'success' && result.url) {
            // Stream URL dari yt-dlp — buka di tab baru, browser/HP akan download otomatis
            showToast('Membuka link download...');
            window.open(result.url, '_blank');
            setTimeout(() => showToast('Jika tidak otomatis, tahan link lalu Simpan'), 1500);
        } else {
            showToast('Gagal: ' + (result.message || 'Coba lagi'));
        }"""

new = """        if (result.status === 'success' && result.url) {
            showToast('Download dimulai...');
            const ext = result.ext || 'mp4';
            const fname = (title || 'lagu') + '.' + ext;
            // Coba download langsung via anchor
            const a = document.createElement('a');
            a.href = result.url;
            a.download = fname;
            a.target = '_blank';
            a.rel = 'noopener noreferrer';
            document.body.appendChild(a);
            a.click();
            setTimeout(() => { document.body.removeChild(a); showToast('Jika tidak tersimpan, tahan link lalu Simpan'); }, 1500);
        } else {
            showToast('Gagal: ' + (result.message || 'Coba lagi'));
        }"""

if old in src:
    src = src.replace(old, new)
    open(r"C:\Users\Admin\Downloads\Auspoty\public\script.js", "w", encoding="utf-8").write(src)
    print("Patched OK")
else:
    print("Not found, checking...")
    idx = src.find("Stream URL dari yt-dlp")
    print("idx:", idx)
    if idx > 0:
        print(repr(src[idx-50:idx+200]))
