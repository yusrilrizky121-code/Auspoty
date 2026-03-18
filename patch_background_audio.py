with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Tambah background keep-alive setelah baris pertama (setelah PWA block)
bg_keepalive = """
// ============================================================
// BACKGROUND AUDIO KEEP-ALIVE
// Mencegah browser throttle tab saat minimize / layar mati
// ============================================================
(function() {
    // 1. Silent AudioContext oscillator — mencegah browser suspend audio
    var _audioCtx = null;
    var _silentNode = null;
    function startSilentAudio() {
        try {
            if (_audioCtx && _audioCtx.state !== 'closed') return;
            _audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            var oscillator = _audioCtx.createOscillator();
            var gainNode = _audioCtx.createGain();
            gainNode.gain.value = 0.001; // hampir tidak terdengar
            oscillator.connect(gainNode);
            gainNode.connect(_audioCtx.destination);
            oscillator.start();
            _silentNode = oscillator;
        } catch(e) {}
    }

    // 2. Screen Wake Lock API — cegah layar/CPU sleep saat musik jalan
    var _wakeLock = null;
    async function requestWakeLock() {
        if ('wakeLock' in navigator) {
            try {
                _wakeLock = await navigator.wakeLock.request('screen');
            } catch(e) {}
        }
    }
    async function releaseWakeLock() {
        if (_wakeLock) { try { await _wakeLock.release(); } catch(e) {} _wakeLock = null; }
    }

    // 3. Saat tab tersembunyi, aktifkan keep-alive
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            startSilentAudio();
            // Resume AudioContext jika suspended
            if (_audioCtx && _audioCtx.state === 'suspended') {
                _audioCtx.resume().catch(function(){});
            }
        } else {
            // Tab kembali aktif — resume AudioContext
            if (_audioCtx && _audioCtx.state === 'suspended') {
                _audioCtx.resume().catch(function(){});
            }
        }
    });

    // 4. Saat musik mulai diputar, aktifkan wake lock
    window._bgAudio = {
        onPlay: function() {
            startSilentAudio();
            requestWakeLock();
            if (_audioCtx && _audioCtx.state === 'suspended') {
                _audioCtx.resume().catch(function(){});
            }
        },
        onPause: function() {
            releaseWakeLock();
        }
    };

    // 5. Re-acquire wake lock saat visibility berubah kembali ke visible
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden && _wakeLock === null) {
            // Cek apakah lagu sedang main
            if (typeof isPlaying !== 'undefined' && isPlaying) {
                requestWakeLock();
            }
        }
    });
})();

"""

# Sisipkan setelah blok PWA (setelah baris window.addEventListener beforeinstallprompt)
insert_after = "deferredPrompt = null; }); }\n});"
if insert_after in content:
    content = content.replace(insert_after, insert_after + "\n" + bg_keepalive, 1)
    print("OK: background keep-alive inserted after PWA block")
else:
    # Fallback: sisipkan di awal setelah komentar PWA
    content = bg_keepalive + content
    print("OK: background keep-alive inserted at top (fallback)")

# 6. Hook ke onPlayerStateChange — panggil _bgAudio.onPlay/onPause
old_playing = "isPlaying = true;\n        if (mainBtn) mainBtn.innerHTML = '<path d=\"' + pausePath + '\"/>';\n        if (miniBtn) miniBtn.innerHTML = '<path d=\"' + pausePath + '\"/>';\n        startProgressBar();"
new_playing = "isPlaying = true;\n        if (mainBtn) mainBtn.innerHTML = '<path d=\"' + pausePath + '\"/>';\n        if (miniBtn) miniBtn.innerHTML = '<path d=\"' + pausePath + '\"/>';\n        startProgressBar();\n        if (window._bgAudio) window._bgAudio.onPlay();"

if old_playing in content:
    content = content.replace(old_playing, new_playing)
    print("OK: onPlay hook added")
else:
    print("WARN: onPlay pattern not found")

old_paused = "isPlaying = false;\n        if (mainBtn) mainBtn.innerHTML = '<path d=\"' + playPath + '\"/>';\n        if (miniBtn) miniBtn.innerHTML = '<path d=\"' + playPath + '\"/>';\n        stopProgressBar();\n    } else if (event.data == YT.PlayerState.ENDED)"
new_paused = "isPlaying = false;\n        if (mainBtn) mainBtn.innerHTML = '<path d=\"' + playPath + '\"/>';\n        if (miniBtn) miniBtn.innerHTML = '<path d=\"' + playPath + '\"/>';\n        stopProgressBar();\n        if (window._bgAudio) window._bgAudio.onPause();\n    } else if (event.data == YT.PlayerState.ENDED)"

if old_paused in content:
    content = content.replace(old_paused, new_paused)
    print("OK: onPause hook added")
else:
    print("WARN: onPause pattern not found, trying alternate...")
    i = content.find("YT.PlayerState.PAUSED")
    print(repr(content[i:i+200]))

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
