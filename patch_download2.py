src = open(r"C:\Users\Admin\Downloads\Auspoty\public\script.js", encoding="utf-8").read()

old = """// DOWNLOAD
async function downloadMusic() {
    if (!currentTrack) return;
    const btn = document.getElementById('downloadBtn');
    const btnMini = document.getElementById('downloadBtnMini');
    const title = (currentTrack.title || 'lagu').replace(/[^a-zA-Z0-9 ]/g, '').trim();

    // Set loading state
    [btn, btnMini].forEach(b => { if (b) { b.style.opacity = '0.4'; b.style.pointerEvents = 'none'; } });
    showToast('Menyiapkan download...');

    try {
        const res = await fetch('/api/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ videoId: currentTrack.videoId })
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            showToast('Server error: ' + (err.message || res.status));
            return;
        }

        const result = await res.json();

        if (result.status === 'success' && result.url) {
            showToast('Download dimulai: ' + (title || 'lagu'));
            // Buka URL download di tab baru — browser/HP akan handle save file
            const a = document.createElement('a');
            a.href = result.url;
            a.download = (title || 'lagu') + '.mp3';
            a.rel = 'noopener';
            a.target = '_blank';
            document.body.appendChild(a);
            a.click();
            setTimeout(() => document.body.removeChild(a), 1000);
        } else {
            showToast('Gagal: ' + (result.message || 'Server tidak merespons'));
        }
    } catch (e) {
        showToast('Gagal koneksi ke server download');
    } finally {
        [btn, btnMini].forEach(b => { if (b) { b.style.opacity = '1'; b.style.pointerEvents = ''; } });
    }
}"""

new = """// DOWNLOAD
async function downloadMusic() {
    if (!currentTrack) return;
    const btn = document.getElementById('downloadBtn');
    const btnMini = document.getElementById('downloadBtnMini');
    const title = (currentTrack.title || 'lagu').replace(/[^a-zA-Z0-9 ]/g, '').trim();

    [btn, btnMini].forEach(b => { if (b) { b.style.opacity = '0.4'; b.style.pointerEvents = 'none'; } });
    showToast('Menyiapkan download...');

    try {
        const res = await fetch('/api/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ videoId: currentTrack.videoId, title: title })
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            showToast('Gagal: ' + (err.message || 'Error ' + res.status));
            return;
        }

        const result = await res.json();

        if (result.status === 'success' && result.url) {
            // Stream URL dari yt-dlp — buka di tab baru, browser/HP akan download otomatis
            showToast('Membuka link download...');
            window.open(result.url, '_blank');
            setTimeout(() => showToast('Jika tidak otomatis, tahan link lalu Simpan'), 1500);
        } else {
            showToast('Gagal: ' + (result.message || 'Coba lagi'));
        }
    } catch (e) {
        showToast('Gagal koneksi ke server');
    } finally {
        [btn, btnMini].forEach(b => { if (b) { b.style.opacity = '1'; b.style.pointerEvents = ''; } });
    }
}"""

if old in src:
    src = src.replace(old, new)
    open(r"C:\Users\Admin\Downloads\Auspoty\public\script.js", "w", encoding="utf-8").write(src)
    print("Patched OK, size:", len(src))
else:
    print("ERROR: string not found, searching...")
    idx = src.find("// DOWNLOAD")
    print("Found at:", idx)
    print(repr(src[idx:idx+200]))
