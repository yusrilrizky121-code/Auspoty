with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Fix ENDED handler — cek isRepeat dulu sebelum next song
# ============================================================
old_ended = "        stopProgressBar(); playNextSimilarSong();\n    }\n}\nfunction updateMediaSession()"
new_ended = """        stopProgressBar();
        if (isRepeat && ytPlayer) {
            // Ulangi lagu yang sama
            ytPlayer.seekTo(0);
            ytPlayer.playVideo();
        } else {
            playNextSimilarSong();
        }
    }
}
function updateMediaSession()"""

if old_ended in content:
    content = content.replace(old_ended, new_ended)
    print("OK: ENDED handler fixed with isRepeat check")
else:
    print("WARN: ENDED pattern not found")
    i = content.find('stopProgressBar(); playNextSimilarSong')
    print(repr(content[i:i+100]))

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done script.js!")

# ============================================================
# 2. Fix home pills — tambah onclick handler
# ============================================================
with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_pills = '''<div class="home-pills">
                <div class="pill active">Semua</div>
                <div class="pill">Musik</div>
                <div class="pill">Podcast</div>
            </div>'''

new_pills = '''<div class="home-pills">
                <div class="pill active" onclick="filterHome('all', this)">Semua</div>
                <div class="pill" onclick="filterHome('music', this)">Musik</div>
                <div class="pill" onclick="filterHome('podcast', this)">Podcast</div>
            </div>'''

if old_pills in html:
    html = html.replace(old_pills, new_pills)
    print("OK: home pills onclick added")
else:
    print("WARN: pills pattern not found")
    i = html.find('home-pills')
    print(repr(html[i:i+300]))

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done index.html!")
