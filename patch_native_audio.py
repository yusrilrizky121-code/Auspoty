content = open('public/script.js', 'r', encoding='utf-8').read()

# Find exact playMusic function and replace ytPlayer.loadVideoById line
old_line = '    if (ytPlayer && ytPlayer.loadVideoById) ytPlayer.loadVideoById(videoId);'
new_block = '''    // Di Android APK — pakai native ExoPlayer supaya audio tetap jalan di background
    if (window.AndroidBridge && typeof window.AndroidBridge.playNative === 'function') {
        window._nativePlaying = false;
        window._nativeLoading = true;
        if (ytPlayer && ytPlayer.stopVideo) ytPlayer.stopVideo();
        window.AndroidBridge.playNative(videoId, currentTrack.title, currentTrack.artist, currentTrack.img || '');
        isPlaying = true;
        if (typeof updatePlayPauseBtn === 'function') updatePlayPauseBtn(true);
    } else {
        if (ytPlayer && ytPlayer.loadVideoById) ytPlayer.loadVideoById(videoId);
    }'''

# Only replace inside playMusic function (first occurrence)
idx = content.find('function playMusic(videoId, encodedData)')
end_idx = content.find('\n};', idx)
func_body = content[idx:end_idx]

if old_line in func_body:
    new_func_body = func_body.replace(old_line, new_block, 1)
    content = content[:idx] + new_func_body + content[end_idx:]
    open('public/script.js', 'w', encoding='utf-8').write(content)
    print('OK: native audio hook added to playMusic')
else:
    print('old_line not found in playMusic. Showing function body:')
    print(repr(func_body[:600]))
