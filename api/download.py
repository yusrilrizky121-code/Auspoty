from http.server import BaseHTTPRequestHandler
import json, urllib.request, urllib.parse, urllib.error

COBALT_API = "https://cobalt.tools/api/json"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            video_id = body.get("videoId", "")
            if not video_id:
                self._json(400, {"status": "error", "message": "videoId required"})
                return

            url = "https://www.youtube.com/watch?v=" + video_id
            payload = json.dumps({
                "url": url,
                "vCodec": "h264",
                "vQuality": "720",
                "aFormat": "mp3",
                "isAudioOnly": True,
                "isNoTTWatermark": True,
                "dubLang": False
            }).encode()

            req = urllib.request.Request(
                COBALT_API,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": "Mozilla/5.0"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read())

            if result.get("status") in ("stream", "redirect", "tunnel", "picker"):
                download_url = result.get("url") or (result.get("picker", [{}])[0].get("url", ""))
                self._json(200, {"status": "success", "url": download_url})
            else:
                self._json(200, {"status": "error", "message": result.get("text", "Gagal mendapatkan link download")})

        except Exception as e:
            self._json(500, {"status": "error", "message": str(e)})

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
