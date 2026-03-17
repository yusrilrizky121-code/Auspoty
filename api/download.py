from http.server import BaseHTTPRequestHandler
import json, subprocess, sys

# Player clients yang bypass YouTube bot check (tested working)
PLAYER_CLIENTS = ["android", "tv_embedded"]

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            video_id = body.get("videoId", "")
            title = body.get("title", "lagu")
            if not video_id:
                self._json(400, {"status": "error", "message": "videoId required"})
                return

            yt_url = "https://www.youtube.com/watch?v=" + video_id
            last_err = "unknown"

            for client in PLAYER_CLIENTS:
                try:
                    result = subprocess.run(
                        [
                            sys.executable, "-m", "yt_dlp",
                            "--get-url",
                            "--format", "bestaudio[ext=m4a]/bestaudio/best",
                            "--no-playlist",
                            "--no-warnings",
                            "--quiet",
                            "--extractor-args", f"youtube:player_client={client}",
                            yt_url
                        ],
                        capture_output=True,
                        text=True,
                        timeout=25
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        stream_url = result.stdout.strip().split("\n")[0]
                        self._json(200, {
                            "status": "success",
                            "url": stream_url,
                            "title": title
                        })
                        return
                    last_err = result.stderr.strip()[:150] if result.stderr else "no output"
                except subprocess.TimeoutExpired:
                    last_err = "timeout"
                    continue
                except Exception as e:
                    last_err = str(e)[:100]
                    continue

            self._json(502, {"status": "error", "message": last_err})

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
