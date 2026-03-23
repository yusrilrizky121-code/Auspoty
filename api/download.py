from http.server import BaseHTTPRequestHandler
import json, urllib.parse

def get_audio_url(video_id):
    """Get direct audio stream URL using yt-dlp android_music client."""
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
                'player_client': ['android_music', 'android'],
            }
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            f'https://www.youtube.com/watch?v={video_id}',
            download=False
        )

    formats = info.get('formats', [])
    # Prefer audio-only formats
    audio = [
        f for f in formats
        if f.get('vcodec') == 'none'
        and f.get('acodec') not in ('none', None)
        and f.get('url')
        and f.get('ext') not in ('mhtml', 'none', None)
        and 'storyboard' not in (f.get('url') or '')
    ]
    if not audio:
        audio = [
            f for f in formats
            if f.get('url')
            and f.get('acodec') not in ('none', None)
            and f.get('ext') not in ('mhtml',)
            and 'storyboard' not in (f.get('url') or '')
        ]
    if not audio:
        raise Exception('No audio format found')

    # Prefer m4a/mp4, fallback to webm
    m4a = [f for f in audio if f.get('ext', '') in ('m4a', 'mp4')]
    chosen = sorted(m4a or audio, key=lambda x: (x.get('abr') or x.get('tbr') or 0), reverse=True)[0]

    ext = chosen.get('ext', 'mp4')
    if ext not in ('mp4', 'm4a', 'webm', 'mp3'):
        ext = 'mp4'

    return {
        'url': chosen['url'],
        'title': info.get('title', video_id),
        'ext': ext,
        'headers': chosen.get('http_headers', {}),
    }


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        video_id = params.get('video_id', params.get('videoId', ['']))[0].strip()
        if not video_id:
            self._json(400, {'status': 'error', 'message': 'video_id required'})
            return
        try:
            result = get_audio_url(video_id)
            self._json(200, {'status': 'success', **result})
        except Exception as e:
            self._json(500, {'status': 'error', 'message': str(e)[:300]})

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
