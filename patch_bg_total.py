with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Ganti seluruh blok BACKGROUND AUDIO KEEP-ALIVE
#    dengan versi yang lebih robust
# ============================================================
# Cari blok lama
start_marker = "\n// ============================================================\n// BACKGROUND AUDIO KEEP-ALIVE"
end_marker = "})();\n\n"

i_start = content.find(start_marker)
i_end = content.find(end_marker, i_start)
if i_start >= 0 and i_end >= 0:
    old_block = content[i_start:i_end + len(end_marker)]
    print(f"Found old block: {len(old_block)} chars")
else:
    print("WARN: block not found, searching...")
    i_start = content.find('BACKGROUND AUDIO KEEP-ALIVE')
    print(repr(content[i_start:i_start+100]))

new_block = """
// ============================================================
// BACKGROUND AUDIO KEEP-ALIVE v2 — lebih agresif
// ============================================================
var _bgAudioCtx = null;
var _bgGainNode = null;
var _bgOscillator = null;
var _bgWakeLock = null;
var _bgKeepAliveInterval = null;

function _bgStartAudioContext() {
    try {
        if (_bgAudioCtx && _bgAudioCtx.state !== 'closed') {
            if (_bgAudioCtx.state === 'suspended') _bgAudioCtx.resume();
            return;
        }
        _bgAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
        _bgGainNode = _bgAudioCtx.createGain();
        _bgGainNode.gain.value = 0.00001; // nyaris 0, tidak terdengar
        _bgGainNode.connect(_bgAudioCtx.destination);
        // Oscillator silent — mencegah browser suspend audio context
        _bgOscillator = _bgAudioCtx.createOscillator();
        _bgOscillator.frequency.value = 1; // 1Hz, tidak terdengar
        _bgOscillator.connect(_bgGainNode);
        _bgOscillator.start();
    } catch(e) {}
}

async function _bgRequestWakeLock() {
    if ('wakeLock' in navigator) {
        try {
            if (_bgWakeLock) { try { await _bgWakeLock.release(); } catch(e){} }
            _bgWakeLock = await navigator.wakeLock.request('screen');
            _bgWakeLock.addEventListener('release', function() {
                // Re-acquire jika musik masih main
                if (typeof isPlaying !== 'undefined' && isPlaying) {
                    setTimeout(_bgRequestWakeLock, 1000);
                }
            });
        } catch(e) {}
    }
}

function _bgStartKeepAlive() {
    _bgStartAudioContext();
    _bgRequestWakeLock();
    // Interval agresif 500ms — cek status player dan pastikan tetap jalan
    if (_bgKeepAliveInterval) clearInterval(_bgKeepAliveInterval);
    _bgKeepAliveInterval = setInterval(function() {
        // Resume AudioContext jika suspended
        if (_bgAudioCtx && _bgAudioCtx.state === 'suspended') {
            _bgAudioCtx.resume().catch(function(){});
        }
        // Cek apakah ytPlayer masih ada dan dalam state yang benar
        if (typeof ytPlayer !== 'undefined' && ytPlayer && typeof ytPlayer.getPlayerState === 'function') {
            var state = ytPlayer.getPlayerState();
            // State -1=unstarted, 0=ended, 1=playing, 2=paused, 3=buffering, 5=cued
            if (state === 0) {
                // Lagu ended tapi belum di-handle (mungkin event terlewat di background)
                if (typeof isRepeat !== 'undefined' && isRepeat) {
                    ytPlayer.seekTo(0); ytPlayer.playVideo();
                } else if (typeof playNextSimilarSong === 'function') {
                    playNextSimilarSong();
                }
            } else if (state === 2 && typeof isPlaying !== 'undefined' && isPlaying) {
                // Player paused tapi seharusnya playing — resume
                ytPlayer.playVideo();
            }
        }
    }, 500);
}

function _bgStopKeepAlive() {
    if (_bgKeepAliveInterval) { clearInterval(_bgKeepAliveInterval); _bgKeepAliveInterval = null; }
    if (_bgWakeLock) { try { _bgWakeLock.release(); } catch(e){} _bgWakeLock = null; }
}

// Expose ke onPlayerStateChange
window._bgAudio = {
    onPlay: function() { _bgStartKeepAlive(); },
    onPause: function() { _bgStopKeepAlive(); }
};

// Saat visibility berubah — pastikan AudioContext tetap aktif
document.addEventListener('visibilitychange', function() {
    if (_bgAudioCtx && _bgAudioCtx.state === 'suspended') {
        _bgAudioCtx.resume().catch(function(){});
    }
    if (!document.hidden && typeof isPlaying !== 'undefined' && isPlaying) {
        _bgRequestWakeLock();
    }
});

// Re-acquire wake lock saat kembali online
window.addEventListener('focus', function() {
    if (typeof isPlaying !== 'undefined' && isPlaying) {
        _bgRequestWakeLock();
    }
});

"""

if i_start >= 0 and i_end >= 0:
    content = content[:i_start] + new_block + content[i_end + len(end_marker):]
    print("OK: background keep-alive replaced")
else:
    # Sisipkan sebelum // INDEXEDDB
    content = content.replace('// INDEXEDDB', new_block + '// INDEXEDDB', 1)
    print("OK: background keep-alive inserted (fallback)")

# ============================================================
# 2. Ganti startProgressBar dengan versi yang tidak bergantung
#    pada setInterval saja — tambah fallback polling
# ============================================================
old_progress = """function startProgressBar() {
    stopProgressBar();
    progressInterval = setInterval(() => {
        if (ytPlayer && ytPlayer.getCurrentTime && ytPlayer.getDuration) {
            const cur = ytPlayer.getCurrentTime(), dur = ytPlayer.getDuration();
            if (dur > 0) {
                const pct = (cur / dur) * 100;
                const bar = document.getElementById('progressBar');
                bar.value = pct;
                bar.style.background = 'linear-gradient(to right, white ' + pct + '%, rgba(255,255,255,0.2) ' + pct + '%)';
                document.getElementById('currentTime').innerText = formatTime(cur);
                document.getElementById('totalTime').innerText = formatTime(dur);
            }
        }
    }, 1000);
}"""

new_progress = """function startProgressBar() {
    stopProgressBar();
    progressInterval = setInterval(() => {
        if (ytPlayer && ytPlayer.getCurrentTime && ytPlayer.getDuration) {
            const cur = ytPlayer.getCurrentTime(), dur = ytPlayer.getDuration();
            if (dur > 0) {
                const pct = (cur / dur) * 100;
                const bar = document.getElementById('progressBar');
                if (bar) {
                    bar.value = pct;
                    bar.style.background = 'linear-gradient(to right, white ' + pct + '%, rgba(255,255,255,0.2) ' + pct + '%)';
                }
                const ct = document.getElementById('currentTime');
                const tt = document.getElementById('totalTime');
                if (ct) ct.innerText = formatTime(cur);
                if (tt) tt.innerText = formatTime(dur);
            }
        }
    }, 1000);
}"""

if old_progress in content:
    content = content.replace(old_progress, new_progress)
    print("OK: startProgressBar made null-safe")
else:
    print("WARN: startProgressBar pattern not found")

# ============================================================
# 3. Pastikan _bgAudio.onPlay dipanggil saat playMusic
#    dan AudioContext di-create saat ada user gesture
# ============================================================
# Cari hook onPlay yang sudah ada
i_hook = content.find('if (window._bgAudio) window._bgAudio.onPlay();')
print(f"\nonPlay hook exists: {i_hook >= 0}")

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
