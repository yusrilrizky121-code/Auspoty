import re

path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
content = open(path, 'r', encoding='utf-8').read()

print(f"Original size: {len(content)}")

# ============================================================
# FIX 1: downloadMusic — pakai AndroidBridge kalau ada, fallback window.open
# ============================================================
old_dl = '''function downloadMusic() {
    if (!currentTrack) { showToast('Putar lagu dulu!'); return; }
    window.open('https://id.ytmp3.mobi/v1/#' + currentTrack.videoId, '_blank');
    showToast('Halaman download dibuka. Klik Konversi lalu Unduh MP3');
}'''

new_dl = '''function downloadMusic() {
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

if old_dl in content:
    content = content.replace(old_dl, new_dl, 1)
    print("✓ Fix 1: downloadMusic updated")
else:
    print("✗ Fix 1: downloadMusic old pattern not found, trying regex...")
    # Coba regex lebih fleksibel
    pattern = r'function downloadMusic\(\)\s*\{[^}]+\}'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_dl + content[match.end():]
        print("✓ Fix 1: downloadMusic updated via regex")
    else:
        print("✗ Fix 1: FAILED - downloadMusic not found")

# ============================================================
# FIX 2: playMusic — tambah window.currentTrack dan AndroidBridge.onMusicPlay
# ============================================================
old_pm = '''function playMusic(videoId, encodedData) {
    currentTrack = JSON.parse(decodeURIComponent(encodedData));
    checkIfLiked(currentTrack.videoId); updateMediaSession();'''

new_pm = '''function playMusic(videoId, encodedData) {
    currentTrack = JSON.parse(decodeURIComponent(encodedData));
    window.currentTrack = currentTrack;
    checkIfLiked(currentTrack.videoId); updateMediaSession();
    // Notify Flutter untuk background audio
    if (window.AndroidBridge && typeof window.AndroidBridge.onMusicPlay === 'function') {
        window.AndroidBridge.onMusicPlay(currentTrack.title, currentTrack.artist);
    }'''

if old_pm in content:
    content = content.replace(old_pm, new_pm, 1)
    print("✓ Fix 2: playMusic updated with window.currentTrack + AndroidBridge.onMusicPlay")
else:
    print("✗ Fix 2: playMusic old pattern not found")
    # Check what's there
    idx = content.find('function playMusic(videoId')
    if idx >= 0:
        print(f"  Found at {idx}: {repr(content[idx:idx+150])}")

# ============================================================
# FIX 3: Pastikan onYouTubeIframeAPIReady / ytPlayer state change
#         panggil AndroidBridge.onMusicPlay saat lagu mulai play
# ============================================================
# Cari onPlayerStateChange
old_state = "case YT.PlayerState.PLAYING:"
if old_state in content:
    # Cek apakah sudah ada AndroidBridge call di sana
    idx = content.find(old_state)
    chunk = content[idx:idx+500]
    if 'AndroidBridge.onMusicPlay' not in chunk and 'onMusicPlay' not in chunk:
        # Tambah setelah PLAYING case
        old_playing = '''case YT.PlayerState.PLAYING:
            isPlaying = true;'''
        new_playing = '''case YT.PlayerState.PLAYING:
            isPlaying = true;
            if (window.AndroidBridge && currentTrack) {
                window.AndroidBridge.onMusicPlay(currentTrack.title || 'Auspoty', currentTrack.artist || '');
            }'''
        if old_playing in content:
            content = content.replace(old_playing, new_playing, 1)
            print("✓ Fix 3: onPlayerStateChange PLAYING updated")
        else:
            print("✗ Fix 3: PLAYING pattern not found exactly")
    else:
        print("✓ Fix 3: onMusicPlay already in PLAYING handler")
else:
    print("✗ Fix 3: YT.PlayerState.PLAYING not found")

# ============================================================
# Tulis hasil
# ============================================================
open(path, 'w', encoding='utf-8').write(content)
print(f"\nFinal size: {len(content)}")
print("File saved!")

# Verifikasi
content2 = open(path, 'r', encoding='utf-8').read()
print(f"\nVerification:")
print(f"  playMusic count: {content2.count('function playMusic(videoId')}")
print(f"  downloadMusic AndroidBridge: {'AndroidBridge.openDownload' in content2}")
print(f"  window.currentTrack: {'window.currentTrack' in content2}")
print(f"  onMusicPlay in playMusic: {'AndroidBridge.onMusicPlay' in content2}")
