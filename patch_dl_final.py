import re

path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_func = '''// DOWNLOAD
async function downloadMusic() {
    if (!currentTrack) { showToast('Putar lagu dulu!'); return; }
    const btn = document.getElementById('downloadBtn');
    const btnMini = document.getElementById('downloadBtnMini');
    [btn, btnMini].forEach(b => { if (b) { b.style.opacity = '0.4'; b.style.pointerEvents = 'none'; } });
    showToast('Menyiapkan MP3... tunggu sebentar');
    try {
        const API = (typeof API_BASE !== 'undefined') ? API_BASE : '';
        const res = await fetch(API + '/api/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ videoId: currentTrack.videoId, title: currentTrack.title })
        });
        const result = await res.json();
        if (result.status === 'success' && result.url) {
            const a = document.createElement('a');
            a.href = result.url;
            a.download = (result.title || currentTrack.title).replace(/[\\/:*?"<>|]/g, '_') + '.mp3';
            a.target = '_blank';
            document.body.appendChild(a);
            a.click();
            setTimeout(() => document.body.removeChild(a), 1000);
            showToast('Download MP3 dimulai!');
        } else {
            showToast('Gagal: ' + (result.message || 'Coba lagi'));
        }
    } catch (e) {
        showToast('Gagal koneksi ke server');
    } finally {
        [btn, btnMini].forEach(b => { if (b) { b.style.opacity = '1'; b.style.pointerEvents = ''; } });
    }
}'''

# Replace existing downloadMusic block
lines = content.split('\n')
start = None
end = None
brace_count = 0
in_func = False

for i, line in enumerate(lines):
    if ('function downloadMusic' in line):
        start = i
        if i > 0 and '// DOWNLOAD' in lines[i-1]:
            start = i - 1
        in_func = True
        brace_count = 0
    if in_func and start is not None:
        brace_count += line.count('{') - line.count('}')
        if brace_count <= 0 and i > start:
            end = i
            break

if start is not None and end is not None:
    new_lines = lines[:start] + new_func.split('\n') + lines[end+1:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    print(f'OK - replaced lines {start}-{end}')
else:
    print('ERROR: function not found')
