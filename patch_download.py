src = open(r"C:\Users\Admin\Downloads\Auspoty\public\script.js", encoding="utf-8").read()

old = """// DOWNLOAD
async function downloadMusic() {
    if (!currentTrack) return;
    const btn = document.getElementById('downloadBtn');
    const btnMini = document.getElementById('downloadBtnMini');
    const title = currentTrack.title || 'lagu';
    showToast('Menyiapkan download...');
    if (btn) { btn.setAttribute('disabled', '1'); btn.style.opacity = '0.5'; }
    if (btnMini) { btnMini.setAttribute('disabled', '1'); btnMini.style.opacity = '0.5'; }
    try {
        const res = await fetch('/api/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ videoId: currentTrack.videoId })
        });
        const result = await res.json();
        if (result.status === 'success' && result.url) {
            showToast('Mengunduh ' + title + '...');
            const a = document.createElement('a');
            a.href = result.url;
            a.download = title.replace(/[^a-zA-Z0-9 ]/g, '') + '.mp3';
            a.target = '_blank';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            setTimeout(() => showToast('Download dimulai!'), 800);
        } else {
            showToast('Gagal: ' + (result.message || 'Coba lagi'));
        }
    } catch (e) {
        showToast('Gagal download. Cek koneksi.');
    } finally {
        if (btn) { btn.removeAttribute('disabled'); btn.style.opacity = '1'; }
        if (btnMini) { btnMini.removeAttribute('disabled'); btnMini.style.opacity = '1'; }
    }
}"""

new = """// DOWNLOAD
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

if old in src:
    src = src.replace(old, new)
    open(r"C:\Users\Admin\Downloads\Auspoty\public\script.js", "w", encoding="utf-8").write(src)
    print("Patched OK, size:", len(src))
else:
    print("ERROR: old string not found!")
    # Find approximate location
    idx = src.find("// DOWNLOAD")
    print("// DOWNLOAD found at index:", idx)
    print("Snippet:", repr(src[idx:idx+100]))
