with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Hook onPlay — panggil AndroidBridge.onMusicPlay
old_onplay = "        if (window._bgAudio) window._bgAudio.onPlay();"
new_onplay = """        if (window._bgAudio) window._bgAudio.onPlay();
        // Beritahu APK agar aktifkan WakeLock + update notifikasi
        if (window.AndroidBridge && currentTrack) {
            try { window.AndroidBridge.onMusicPlay(currentTrack.title || 'Auspoty', currentTrack.artist || ''); } catch(e) {}
        }"""

if old_onplay in content:
    content = content.replace(old_onplay, new_onplay)
    print("OK: AndroidBridge.onMusicPlay hooked")
else:
    print("WARN: onPlay hook not found")

# Hook onPause
old_onpause = "        if (window._bgAudio) window._bgAudio.onPause();"
new_onpause = """        if (window._bgAudio) window._bgAudio.onPause();
        if (window.AndroidBridge) { try { window.AndroidBridge.onMusicPause(); } catch(e) {} }"""

if old_onpause in content:
    content = content.replace(old_onpause, new_onpause)
    print("OK: AndroidBridge.onMusicPause hooked")
else:
    print("WARN: onPause hook not found")

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
