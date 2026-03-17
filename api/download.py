from http.server import BaseHTTPRequestHandler
import json, urllib.request, ssl

# Cobalt v10/v11 instances yang support YouTube (dari instances.cobalt.best)
COBALT_INSTANCES = [
    "https://cobalt-api.meowing.de",
    "https://capi.3kh0.net",
]

def cobalt_request(instance, yt_url):
    payload = json.dumps({
        "url": yt_url,
        "downloadMode": "audio",
        "audioFormat": "mp3",
        "audioBitrate": "128",
        "filenameStyle": "basic"
    }).encode()
    req = urllib.request.Request(
        instance + "/",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Auspoty/1.0 (+https://github.com/yusrilrizky121-code/clone2)"
        },
        method="POST"
    )
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        return json.loads(resp.read())

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            video_id = body.get("videoId", "")
            if not video_id:
                self._json(400, {"status": "error", "message": "videoId required"})
                return

            yt_url = "https://www.youtube.com/watch?v=" + video_id
            last_error = "Semua server gagal"

            for instance in COBALT_INSTANCES:
                try:
                    result = cobalt_request(instance, yt_url)
                    status = result.get("status", "")

                    if status in ("tunnel", "redirect", "stream"):
                        dl_url = result.get("url", "")
                        if dl_url:
                            self._json(200, {"status": "success", "url": dl_url})
                            return

                    elif status == "picker":
                        items = result.get("picker", [])
                        if items and items[0].get("url"):
                            self._json(200, {"status": "success", "url": items[0]["url"]})
                            return

                    # Extract error message from cobalt v10/v11 format
                    err = result.get("error", {})
                    if isinstance(err, dict):
                        last_error = err.get("code", str(result))
                    else:
                        last_error = str(err or result.get("text", "unknown"))

                except Exception as e:
                    last_error = str(e)[:100]
                    continue

            self._json(502, {"status": "error", "message": "Gagal: " + last_error})

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
