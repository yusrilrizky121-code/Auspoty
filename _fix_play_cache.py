import os

BASE = r'C:\Users\Admin\Downloads\Auspoty'
JS = os.path.join(BASE, 'public', 'script.js')

with open(JS, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Tambah _trackCache dan playMusicById setelah makeTrackData
old_make = "function makeTrackData(t) {\n    const img = getHighResImage(t.thumbnail || t.img || '');\n    return encodeURIComponent(JSON.stringify({ videoId: t.videoId, title: t.title, artist: t.artist || 'Unknown', img }));\n}"

new_make = """function makeTrackData(t) {
    const img = getHighResImage(t.thumbnail || t.img || '');
    return encodeURIComponent(JSON.stringify({ videoId: t.videoId, title: t.title, artist: t.artist || 'Unknown', img }));
}

// TRACK CACHE - simpan track object supaya onclick tidak perlu encode string panjang
window._trackCache = window._trackCache || {};
function _cacheTrack(t) {
    const img = getHighResImage(t.thumbnail || t.img || '');
    window._trackCache[t.videoId] = { videoId: t.videoId, title: t.title || '', artist: t.artist || 'Unknown', img };
}
function playMusicById(videoId) {
    const t = window._trackCache[videoId];
    if (t) {
        playMusic(t.videoId, makeTrackData(t));
    } else {
        // fallback: coba play langsung dengan videoId saja
        if (ytPlayer && ytPlayer.loadVideoById) {
            document.getElementById('miniPlayer').style.display = 'flex';
            ytPlayer.loadVideoById(videoId);
        }
    }
}"""

if old_make in content:
    content = content.replace(old_make, new_make)
    print('Fix 1 OK: added _trackCache and playMusicById')
else:
    print('Fix 1 FAILED: makeTrackData not found')
    idx = content.find('function makeTrackData')
    print(repr(content[idx:idx+200]))

# 2. Patch renderVItem - ganti onclick ke playMusicById
old_rv_onclick = 'return \'<div class="v-item" onclick="playMusic(\\\'\' + t.videoId + \'\\\',\\\'\' + d + \'\\\')">\''
new_rv_onclick = '_cacheTrack(t);\n    return \'<div class="v-item" onclick="playMusicById(\\\'\' + t.videoId + \'\\\')">\''

# 3. Patch renderHCard - ganti onclick ke playMusicById
old_rh_onclick = 'return \'<div class="h-card" onclick="playMusic(\\\'\' + t.videoId + \'\\\',\\\'\' + d + \'\\\')">\''
new_rh_onclick = '_cacheTrack(t);\n    return \'<div class="h-card" onclick="playMusicById(\\\'\' + t.videoId + \'\\\')">\''

# Also need to remove "const d = makeTrackData(t);" from renderVItem and renderHCard
# since d is no longer used

if old_rv_onclick in content:
    content = content.replace(old_rv_onclick, new_rv_onclick)
    content = content.replace(
        'function renderVItem(t) {\n    const d = makeTrackData(t);\n    ' + new_rv_onclick,
        'function renderVItem(t) {\n    ' + new_rv_onclick
    )
    print('Fix 2 OK: renderVItem uses playMusicById')
else:
    print('Fix 2 FAILED: renderVItem onclick not found')
    idx = content.find('function renderVItem')
    print(repr(content[idx:idx+250]))

if old_rh_onclick in content:
    content = content.replace(old_rh_onclick, new_rh_onclick)
    content = content.replace(
        'function renderHCard(t) {\n    const d = makeTrackData(t);\n    ' + new_rh_onclick,
        'function renderHCard(t) {\n    ' + new_rh_onclick
    )
    print('Fix 3 OK: renderHCard uses playMusicById')
else:
    print('Fix 3 FAILED: renderHCard onclick not found')
    idx = content.find('function renderHCard')
    print(repr(content[idx:idx+250]))

with open(JS, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify syntax
import subprocess
result = subprocess.run(['node', '-e', f'try{{new Function(require("fs").readFileSync(String.raw`{JS}`,"utf8"));console.log("SYNTAX OK")}}catch(e){{console.log("ERROR:",e.message)}}'], capture_output=True, text=True)
print(result.stdout.strip())
print('DONE')
