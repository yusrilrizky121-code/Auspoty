path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
content = open(path, 'r', encoding='utf-8').read()

old = '''function downloadMusic() {
    if (!currentTrack) { showToast('Putar lagu dulu!'); return; }
    const url = 'https://id.ytmp3.mobi/v1/#' + currentTrack.videoId;
    if (window.AndroidBridge && typeof window.AndroidBridge.openDownload === 'function') {
        window.AndroidBridge.openDownload(url);
        showToast('Membuka download di browser...');
    } else {
        window.open(url, '_blank');
        showToast('Halaman download dibuka. Klik Konversi lalu Unduh MP3');
    }
}'''

new = '''function downloadMusic() {
    if (!currentTrack) { showToast('Putar lagu dulu!'); return; }
    if (window.AndroidBridge && typeof window.AndroidBridge.openDownload === 'function') {
        // Di APK Flutter: download langsung ke storage tanpa buka browser
        showToast('Mengunduh ' + (currentTrack.title || 'lagu') + '...');
        window.AndroidBridge.openDownload(currentTrack.videoId, currentTrack.title || '');
    } else {
        // Di browser biasa: buka halaman download
        window.open('https://id.ytmp3.mobi/v1/#' + currentTrack.videoId, '_blank');
        showToast('Halaman download dibuka. Klik Konversi lalu Unduh MP3');
    }
}'''

if old in content:
    content = content.replace(old, new, 1)
    print('✓ downloadMusic updated')
else:
    # Coba cari versi yang ada
    import re
    m = re.search(r'function downloadMusic\(\)\s*\{.*?\n\}', content, re.DOTALL)
    if m:
        print('Found via regex:')
        print(repr(m.group(0)[:300]))
        content = content[:m.start()] + new + content[m.end():]
        print('✓ downloadMusic updated via regex')
    else:
        print('✗ downloadMusic not found!')

open(path, 'w', encoding='utf-8').write(content)
print('Saved.')
print('Verify:', 'openDownload(currentTrack.videoId' in content)
