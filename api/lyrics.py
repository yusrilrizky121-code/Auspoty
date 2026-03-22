import json
import re
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler

def parse_lrc(lrc_text):
    lines = []
    pattern = re.compile(r'\[(\d+):(\d+\.\d+)\](.*)')
    for line in lrc_text.split('\n'):
        m = pattern.match(line.strip())
        if m:
            t = int(m.group(1)) * 60 + float(m.group(2))
            text = m.group(3).strip()
            if text:
                lines.append({"time": t, "text": text})
    return lines

def get_lyrics_lrclib(title, artist):
    try:
        params = urllib.parse.urlencode({"track_name": title, "artist_name": artist})
        req = urllib.request.Request(
            "https://lrclib.net/api/get?" + params,
            headers={"User-Agent": "Auspoty/1.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
        synced = data.get("syncedLyrics", "")
        plain = data.get("plainLyrics", "")
        if synced:
            return {"type": "synced", "lines": parse_lrc(synced)}
        elif plain:
            lines = [l.strip() for l in plain.split('\n') if l.strip()]
            return {"type": "plain", "lines": [{"time": None, "text": l} for l in lines]}
    except Exception:
        pass
    return None

def get_title_artist_from_yt(video_id):
    """Get title/artist from YouTube oEmbed (no API key needed)"""
    try:
        url = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=" + video_id + "&format=json"
        with urllib.request.urlopen(url, timeout=8) as r:
            data = json.loads(r.read().decode())
        title = data.get("title", "")
        author = data.get("author_name", "")
        # Strip " - Topic" suffix common on YouTube Music
        artist = author.replace(" - Topic", "").strip()
        return title, artist
    except Exception:
        return "", ""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        video_id = params.get('video_id', [''])[0]

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        if not video_id:
            self.wfile.write(json.dumps({"status": "error", "message": "video_id required"}).encode())
            return

        try:
            title, artist = get_title_artist_from_yt(video_id)
            if title:
                result = get_lyrics_lrclib(title, artist)
                if result:
                    self.wfile.write(json.dumps({"status": "success", "data": result}).encode())
                    return
            self.wfile.write(json.dumps({"status": "error", "message": "Lirik tidak ditemukan"}).encode())
        except Exception as e:
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
