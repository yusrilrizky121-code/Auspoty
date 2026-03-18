with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix makeTrackData - tambah sanitasi title dan artist sebelum encode
# Masalah: title seperti "Beautiful in White" bisa punya karakter yang break onclick HTML
# Solusi: strip karakter yang bisa break HTML attribute sebelum JSON.stringify

old_make = """function makeTrackData(t) {
    const img = getHighResImage(t.thumbnail || t.img || '');
    return encodeURIComponent(JSON.stringify({ videoId: t.videoId, title: t.title, artist: t.artist || 'Unknown', img }));
}"""

new_make = """function makeTrackData(t) {
    const img = getHighResImage(t.thumbnail || t.img || '');
    // Sanitasi title & artist: hapus karakter yang bisa break HTML onclick attribute
    const title = (t.title || '').replace(/['"\\\\]/g, ' ').trim();
    const artist = (t.artist || 'Unknown').replace(/['"\\\\]/g, ' ').trim();
    return encodeURIComponent(JSON.stringify({ videoId: t.videoId, title: title, artist: artist, img }));
}"""

if old_make in content:
    content = content.replace(old_make, new_make)
    print('Fix makeTrackData OK')
else:
    print('makeTrackData not found exactly, trying partial...')
    # Try to find and show context
    idx = content.find('function makeTrackData')
    if idx != -1:
        print(repr(content[idx:idx+200]))

# Fix renderVItem - ganti cara onclick supaya lebih aman
# Pakai data attribute + window._trackMap untuk hindari HTML injection
old_render_v = """function renderVItem(t) {
    const d = makeTrackData(t);
    return '<div class="v-item" onclick="playMusic(\\'' + t.videoId + '\\',\\'' + d + '\\')">'+
        '<img class="v-img" src="' + getHighResImage(t.thumbnail || t.img || '') + '" onerror="this.src=\\'https://via.placeholder.com/48x48?text=music\\'">'+
        '<div class="v-info"><div class="v-title">' + (t.title || '') + '</div><div class="v-sub">' + (t.artist || '') + '</div></div>'+
        '<svg class="dots-icon" viewBox="0 0 24 24"><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg>'+
        '</div>';
}"""

# Simpler approach: patch playMusic to be more robust
# and use window._trackCache to store track data by videoId

inject_cache = """
// TRACK CACHE - simpan data lagu supaya onclick tidak perlu encode/decode
window._trackCache = window._trackCache || {};
function _cacheTrack(t) {
    const img = getHighResImage(t.thumbnail || t.img || '');
    const track = { videoId: t.videoId, title: t.title || '', artist: t.artist || 'Unknown', img };
    window._trackCache[t.videoId] = track;
    return t.videoId;
}
"""

# Patch renderVItem to use cache
old_v = "function renderVItem(t) {\n    const d = makeTrackData(t);\n    return '<div class=\"v-item\" onclick=\"playMusic(\\'' + t.videoId + '\\',\\'' + d + '\\')\">'"
new_v = "function renderVItem(t) {\n    _cacheTrack(t);\n    return '<div class=\"v-item\" onclick=\"playMusicById(\\'' + t.videoId + '\\')\">'"

old_h = "function renderHCard(t) {\n    const d = makeTrackData(t);\n    return '<div class=\"h-card\" onclick=\"playMusic(\\'' + t.videoId + '\\',\\'' + d + '\\')\">'"
new_h = "function renderHCard(t) {\n    _cacheTrack(t);\n    return '<div class=\"h-card\" onclick=\"playMusicById(\\'' + t.videoId + '\\')\">'"

# Check what's actually in the file
idx_v = content.find('function renderVItem')
idx_h = content.find('function renderHCard')
print('renderVItem at:', idx_v)
print('renderHCard at:', idx_h)
if idx_v != -1:
    print('renderVItem context:', repr(content[idx_v:idx_v+200]))

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('DONE - check output above')
