from http.server import BaseHTTPRequestHandler
import json, urllib.parse

def get_stream_url(video_id):
    import yt_dlp

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp4]/bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,
        'noplaylist': True,
        'extractor_args': {
            'youtube': {
                # android_music return URL yang bisa diakses tanpa header khusus
                'player_client': ['android_music', 'android'],
            }
        },
    }

    url = f'https://www.youtube.com/watch?v={video_id}'
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Ambil format audio terbaik
    formats = info.get('formats', [])
    audio_formats = [
        f for f in formats
        if f.get('vcodec') == 'none'
        and f.get('acodec') not in ('none', None)
        and f.get('url')
        and f.get('ext') not in ('mhtml', 'none', None)
        and 'storyboard' not in (f.get('url') or '')
    ]

    if not audio_formats:
        # Fallback: format dengan audio apapun
        audio_formats = [
            f for f in formats
            if f.get('url')
            and f.get('acodec') not in ('none', None)
            and f.get('ext') not in ('mhtml',)
            and 'storyboard' not in (f.get('url') or '')
        ]

    if not audio_formats:
        raise Exception('No playable format found')

    # Pilih m4a/mp4 dulu, fallback ke webm
    m4a = [f for f in audio_formats if 'm4a' in f.get('ext', '') or 'mp4' in f.get('ext', '')]
    chosen = sorted(m4a or audio_formats, key=lambda x: (x.get('abr') or x.get('tbr') or 0), reverse=True)[0]

    thumbs = info.get('thumbnails', [])
    thumbnail = thumbs[-1]['url'] if thumbs else ''

    # Ambil http_headers dari format yang dipilih (untuk Android MediaPlayer)
    http_headers = chosen.get('http_headers', {})

    return {
        'url': chosen['url'],
        'title': info.get('title', video_id),
        'artist': info.get('uploader', info.get('channel', '')),
        'duration': int(info.get('duration', 0)),
        'thumbnail': thumbnail,
        'mimeType': f"audio/{chosen.get('ext', 'mp4')}",
        'bitrate': int(chosen.get('abr', 0) or chosen.get('tbr', 0) or 0),
        'headers': http_headers,
    }


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            video_id = body.get('videoId', '').strip()
            if not video_id:
                self._json(400, {'status': 'error', 'message': 'videoId required'})
                return
            result = get_stream_url(video_id)
            self._json(200, {'status': 'success', **result})
        except Exception as e:
            self._json(500, {'status': 'error', 'message': str(e)[:300]})

    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        video_id = params.get('videoId', [''])[0].strip()
        if not video_id:
            self._json(400, {'status': 'error', 'message': 'videoId required'})
            return
        try:
            result = get_stream_url(video_id)
            self._json(200, {'status': 'success', **result})
        except Exception as e:
            self._json(500, {'status': 'error', 'message': str(e)[:300]})

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
