with open('public/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# ============================================================
# FIX 1: playMusic() jangan reset _autoQueue
# Queue harus dipertahankan antar lagu, bukan di-reset
# ============================================================
old_playmusic_queue = '''    // Pre-fetch lagu berikutnya di background saat lagu mulai
    _autoQueue = []; // reset queue untuk artis baru
    setTimeout(() => {
        if (currentTrack) prefetchNextSongs(currentTrack.artist, currentTrack.videoId);
    }, 3000); // tunggu 3 detik setelah lagu mulai'''

new_playmusic_queue = '''    // Pre-fetch lagu berikutnya di background saat lagu mulai
    // JANGAN reset _autoQueue — pertahankan queue yang sudah ada
    // Hanya refill jika queue hampir kosong
    setTimeout(() => {
        if (currentTrack && _autoQueue.length < 2) {
            prefetchNextSongs(currentTrack.artist, currentTrack.videoId);
        }
    }, 2000); // tunggu 2 detik setelah lagu mulai'''

if old_playmusic_queue in js:
    js = js.replace(old_playmusic_queue, new_playmusic_queue)
    print('OK: playMusic queue reset removed')
else:
    print('WARN: playMusic queue block not found exactly')
    # Coba cari versi lain
    if '_autoQueue = []; // reset queue untuk artis baru' in js:
        js = js.replace(
            '_autoQueue = []; // reset queue untuk artis baru',
            '// _autoQueue dipertahankan antar lagu (tidak di-reset)'
        )
        print('OK: partial fix - queue reset removed')

# ============================================================
# FIX 2: prefetchNextSongs — threshold lebih agresif
# Refill kalau queue < 5 (bukan >= 3 baru stop)
# ============================================================
old_prefetch_check = 'async function prefetchNextSongs(artist, currentVideoId) {\n    if (_queueFetching || _autoQueue.length >= 3) return;'
new_prefetch_check = 'async function prefetchNextSongs(artist, currentVideoId) {\n    if (_queueFetching || _autoQueue.length >= 5) return;'

if old_prefetch_check in js:
    js = js.replace(old_prefetch_check, new_prefetch_check)
    print('OK: prefetch threshold increased to 5')
else:
    print('WARN: prefetch check not found')

# ============================================================
# FIX 3: playNextSimilarSong — setelah ambil dari queue, 
# langsung trigger refill tanpa delay (bukan 500ms)
# Dan jangan reset queue di playMusic
# ============================================================
old_next = '''function playNextSimilarSong() {
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
}'''

new_next = '''function playNextSimilarSong() {
    if (!currentTrack) return;
    // Ambil dari queue yang sudah di-fetch sebelumnya
    if (_autoQueue.length > 0) {
        const next = _autoQueue.shift(); // ambil dari depan
        // Langsung refill queue sebelum playMusic (agar tidak kosong saat lagu berikutnya selesai)
        prefetchNextSongs(next.artist, next.videoId);
        playMusic(next.videoId, encodeURIComponent(JSON.stringify(next)));
        return;
    }
    // Fallback: coba fetch langsung
    _fetchAndPlayNext(currentTrack.artist, currentTrack.videoId);
}'''

if old_next in js:
    js = js.replace(old_next, new_next)
    print('OK: playNextSimilarSong refill logic fixed')
else:
    print('WARN: playNextSimilarSong not found exactly')

# ============================================================
# FIX 4: _bgKeepAliveInterval — saat state ENDED di background,
# jangan langsung panggil playNextSimilarSong() karena bisa race condition
# Tambah flag _bgHandlingEnded agar tidak dipanggil 2x
# ============================================================
old_bg_ended = '''            if (state === 0) {
                // Lagu ended tapi belum di-handle (mungkin event terlewat di background)
                if (typeof isRepeat !== 'undefined' && isRepeat) {
                    ytPlayer.seekTo(0); ytPlayer.playVideo();
                } else if (typeof playNextSimilarSong === 'function') {
                    playNextSimilarSong();
                }
            } else if (state === 2 && typeof isPlaying !== 'undefined' && isPlaying) {
                // Player paused tapi seharusnya playing — resume
                ytPlayer.playVideo();
            }'''

new_bg_ended = '''            if (state === 0) {
                // Lagu ended tapi belum di-handle (mungkin event terlewat di background)
                // Gunakan flag agar tidak dipanggil berkali-kali
                if (!window._bgEndedHandling) {
                    window._bgEndedHandling = true;
                    if (typeof isRepeat !== 'undefined' && isRepeat) {
                        ytPlayer.seekTo(0); ytPlayer.playVideo();
                        setTimeout(function(){ window._bgEndedHandling = false; }, 3000);
                    } else if (typeof playNextSimilarSong === 'function') {
                        playNextSimilarSong();
                        setTimeout(function(){ window._bgEndedHandling = false; }, 5000);
                    }
                }
            } else if (state === 1 || state === 3) {
                // Sedang playing atau buffering — reset flag
                window._bgEndedHandling = false;
            } else if (state === 2 && typeof isPlaying !== 'undefined' && isPlaying) {
                // Player paused tapi seharusnya playing — resume
                ytPlayer.playVideo();
            }'''

if old_bg_ended in js:
    js = js.replace(old_bg_ended, new_bg_ended)
    print('OK: background ended handler fixed with flag')
else:
    print('WARN: bg ended block not found exactly')

# ============================================================
# FIX 5: onPlayerStateChange ENDED — juga set flag reset
# ============================================================
old_ended_handler = '''    } else if (event.data == YT.PlayerState.ENDED) {
        isPlaying = false;
        if (mainBtn) mainBtn.innerHTML = '<path d="' + playPath + '"/>';
        if (miniBtn) miniBtn.innerHTML = '<path d="' + playPath + '"/>';
        stopProgressBar();
        if (isRepeat && ytPlayer) {
            // Ulangi lagu yang sama
            ytPlayer.seekTo(0);
            ytPlayer.playVideo();
        } else {
            playNextSimilarSong();
        }
    }'''

new_ended_handler = '''    } else if (event.data == YT.PlayerState.ENDED) {
        isPlaying = false;
        if (mainBtn) mainBtn.innerHTML = '<path d="' + playPath + '"/>';
        if (miniBtn) miniBtn.innerHTML = '<path d="' + playPath + '"/>';
        stopProgressBar();
        window._bgEndedHandling = true; // set flag agar bg interval tidak double-trigger
        if (isRepeat && ytPlayer) {
            ytPlayer.seekTo(0);
            ytPlayer.playVideo();
            setTimeout(function(){ window._bgEndedHandling = false; }, 3000);
        } else {
            playNextSimilarSong();
            setTimeout(function(){ window._bgEndedHandling = false; }, 5000);
        }
    }'''

if old_ended_handler in js:
    js = js.replace(old_ended_handler, new_ended_handler)
    print('OK: onPlayerStateChange ENDED flag added')
else:
    print('WARN: ENDED handler not found exactly')

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('script.js saved.')
print('DONE.')
