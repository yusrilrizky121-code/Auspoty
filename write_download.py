content = r'''from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error

INVIDIOUS_INSTANCES = [
    "https://yewtu.be",
    "https://invidious.nerdvpn.de",
    "https://inv.nadeko.net",
]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        video_id = (params.get("videoId") or params.get("videoid") or [""])[0].strip()
        title = (params.get("title") or ["lagu"])[0].strip()
        if not video_id:
            self._json(400, {"status": "error", "message": "videoId required"})
            return
        audio_info = self._get_audio_info(video_id)
        if not audio_info:
            self._json(502, {"status": "error", "message": "Tidak dapat mengambil audio"})
            return
        try:
            req = urllib.request.Request(
                audio_info["url"],
                headers={"User-Agent": "Mozilla/5.0 (compatible; Auspoty/1.0)"}
            )
            with urllib.request.urlopen(req, timeout=30) as audio_resp:
                content_type = audio_resp.headers.get("Content-Type", "audio/webm")
                content_length = audio_resp.headers.get("Content-Length", "")
                ext = audio_info.get("ext", "webm")
                safe_title = (audio_info.get("title") or title).replace('"', "'")
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Disposition",
                    'attachment; filename="' + safe_title + '.' + ext + '"')
                if content_length:
                    self.send_header("Content-Length", content_length)
                self._cors()
                self.end_headers()
                while True:
                    chunk = audio_resp.read(65536)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        except Exception as e:
            self._json(502, {"status": "error", "message": str(e)[:200]})

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            video_id = body.get("videoId", "").strip()
            title = body.get("title", "lagu")
            if not video_id:
                self._json(400, {"status": "error", "message": "videoId required"})
                return
            audio_info = self._get_audio_info(video_id)
            if audio_info:
                self._json(200, {
                    "status": "success",
                    "url": audio_info["url"],
                    "title": audio_info.get("title") or title,
                    "ext": audio_info.get("ext", "webm"),
                })
            else:
                self._json(502, {"status": "error", "message": "Tidak dapat mengambil audio"})
        except Exception as e:
            self._json(500, {"status": "error", "message": str(e)[:200]})

    def _get_audio_info(self, video_id):
        for instance in INVIDIOUS_INSTANCES:
            try:
                url = instance + "/api/v1/videos/" + video_id + "?fields=title,adaptiveFormats"
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (compatible; Auspoty/1.0)",
                        "Accept": "application/json",
                    }
                )
                with urllib.request.urlopen(req, timeout=12) as resp:
                    data = json.loads(resp.read().decode())
                formats = data.get("adaptiveFormats", [])
                audio_formats = [
                    f for f in formats
                    if f.get("type", "").startswith("audio/") and f.get("url")
                ]
                if not audio_formats:
                    continue
                def get_bitrate(f):
                    try:
                        return int(f.get("bitrate", "0"))
                    except Exception:
                        return 0
                audio_formats.sort(key=get_bitrate, reverse=True)
                best = audio_formats[0]
                mime = best.get("type", "audio/webm")
                ext = "webm"
                if "mp4" in mime or "m4a" in mime:
                    ext = "m4a"
                elif "opus" in mime:
                    ext = "opus"
                return {"url": best["url"], "title": data.get("title", ""), "ext": ext}
            except Exception:
                continue
        return None

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
'''

with open(r'api/download.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK - api/download.py written')
