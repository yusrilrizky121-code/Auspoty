with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Ganti playNextSimilarSong dengan sistem queue pre-loaded
# ============================================================
old_fn = """async function playNextSimilarSong() {
    if (!currentTrack) return;
    try {
        const res = await apiFetch('/api/search?query=' + encodeURIComponent(currentTrack.artist + ' official audio'));
        const result = await res.json();
        if (result.status === 'success' && result.data.length > 0) {
            const related = result.data.filter(t => t.videoId !== currentTrack.videoId);
            if (related.length > 0) {
                const next = related[Math.floor(Math.random() * related.length)];
                const img = getHighResImage(next.thumbnail || next.img || '');
                playMusic(next.videoId, encodeURIComponent(JSON.stringify({ videoId: next.videoId, title: next.title, artist: next.artist || 'Unknown', img })));
            }
        }
    } catch (e) {}
}"""

new_fn = """// ============================================================
// AUTO-QUEUE: pre-load lagu berikutnya saat lagu sedang main
// Sehingga saat ENDED tidak perlu fetch lagi (aman di background)
// ============================================================
let _autoQueue = [];       // queue lagu yang sudah di-fetch
let _queueFetching = false;

async function prefetchNextSongs(artist, currentVideoId) {
    if (_queueFetching || _autoQueue.length >= 3) return;
    _queueFetching = true;
    try {
        const res = await apiFetch('/api/search?query=' + encodeURIComponent(artist + ' official audio'));
        const result = await res.json();
        if (result.status === 'success' && result.data.length > 0) {
            const related = result.data.filter(t => t.videoId !== currentVideoId);
            // Shuffle dan ambil 5 lagu, simpan ke queue
            const shuffled = related.sort(() => Math.random() - 0.5).slice(0, 5);
            shuffled.forEach(t => {
                if (!_autoQueue.find(q => q.videoId === t.videoId)) {
                    const img = getHighResImage(t.thumbnail || t.img || '');
                    _autoQueue.push({ videoId: t.videoId, title: t.title, artist: t.artist || 'Unknown', img });
                }
            });
        }
    } catch(e) {}
    _queueFetching = false;
}

function playNextSimilarSong() {
    if (!currentTrack) return;
    // Ambil dari queue yang sudah di-fetch sebelumnya
    if (_autoQueue.length > 0) {
        const next = _autoQueue.shift(); // ambil dari depan
        playMusic(next.videoId, encodeURIComponent(JSON.stringify(next)));
        // Refill queue di background (tidak blocking)
        setTimeout(() => prefetchNextSongs(next.artist, next.videoId), 500);
        return;
    }
    // Fallback: coba fetch langsung (mungkin masih foreground)
    _fetchAndPlayNext(currentTrack.artist, currentTrack.videoId);
}

async function _fetchAndPlayNext(artist, currentVideoId) {
    try {
        const res = await apiFetch('/api/search?query=' + encodeURIComponent(artist + ' official audio'));
        const result = await res.json();
        if (result.status === 'success' && result.data.length > 0) {
            const related = result.data.filter(t => t.videoId !== currentVideoId);
            if (related.length > 0) {
                const next = related[Math.floor(Math.random() * related.length)];
                const img = getHighResImage(next.thumbnail || next.img || '');
                playMusic(next.videoId, encodeURIComponent(JSON.stringify({ videoId: next.videoId, title: next.title, artist: next.artist || 'Unknown', img })));
            }
        }
    } catch(e) {}
}"""

if old_fn in content:
    content = content.replace(old_fn, new_fn)
    print("OK: playNextSimilarSong replaced with queue system")
else:
    print("WARN: playNextSimilarSong pattern not found")
    i = content.find('async function playNextSimilarSong')
    print(repr(content[i:i+200]))

# ============================================================
# 2. Hook ke playMusic — saat lagu mulai, langsung pre-fetch queue
# ============================================================
old_playmusic_end = "    if (ytPlayer && ytPlayer.loadVideoById) ytPlayer.loadVideoById(videoId);\n}"

new_playmusic_end = """    if (ytPlayer && ytPlayer.loadVideoById) ytPlayer.loadVideoById(videoId);
    // Pre-fetch lagu berikutnya di background saat lagu mulai
    _autoQueue = []; // reset queue untuk artis baru
    setTimeout(() => {
        if (currentTrack) prefetchNextSongs(currentTrack.artist, currentTrack.videoId);
    }, 3000); // tunggu 3 detik setelah lagu mulai
}"""

if old_playmusic_end in content:
    content = content.replace(old_playmusic_end, new_playmusic_end)
    print("OK: playMusic hooked to prefetch queue")
else:
    print("WARN: playMusic end pattern not found")
    i = content.find('ytPlayer.loadVideoById(videoId)')
    print(repr(content[i:i+100]))

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
