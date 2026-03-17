src = open(r"C:\Users\Admin\Downloads\Auspoty\public\script.js", encoding="utf-8").read()

download_code = r"""
// DOWNLOAD
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
}
"""

# Insert before INIT section
src = src.replace("// INIT\n", download_code + "\n// INIT\n")
open(r"C:\Users\Admin\Downloads\Auspoty\public\script.js", "w", encoding="utf-8").write(src)
print("Done, size:", len(src))
