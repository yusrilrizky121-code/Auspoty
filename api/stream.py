from http.server import BaseHTTPRequestHandler
import json, urllib.request, urllib.parse, re

# Ambil direct audio stream URL dari YouTube tanpa yt-dlp
# Pakai YouTube's internal API (sama yang dipakai ytmusicapi)

INNERTUBE_KEY = 'AIzaSyA8eiZmM1FaDVjRy-df2KTyQ_vz_yYM39w'
INNERTUBE_CLIENT = {
    'clientName': 'ANDROID_MUSIC',
    'clientVersion': '6.42.52',
    'androidSdkVersion': 30,
    'userAgent': 'com.google.android.apps.youtube.music/6.42.52 (Linux; U; Android 11) gzip',
    'hl': 'id',
    'gl': 'ID',
}

def get_stream_url(video_id):
    url = 'https://music.youtube.com/youtubei/v1/player?key=' + INNERTUBE_KEY
    payload = json.dumps({
        'videoId': video_id,
        'context': {
            'client': INNERTUBE_CLIENT
        },
        'playbackContext': {
            'contentPlaybackContext': {
                'signatureTimestamp': 19950
            }
        }
    }).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': INNERTUBE_CLIENT['userAgent'],
            'X-Goog-Api-Key': INNERTUBE_KEY,
            'Origin': 'https://music.youtube.com',
            'Referer': 'https://music.youtube.com/',
        }
    )

    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read().decode())

    # Ambil streaming formats
    formats = data.get('streamingData', {}).get('adaptiveFormats', [])
    if not formats:
        formats = data.get('streamingData', {}).get('formats', [])

    # Filter audio only, pilih kualitas terbaik
    audio_formats = [f for f in formats if f.get('mimeType', '').startswith('audio/')]
    if not audio_formats:
        raise Exception('No audio formats found')

    # Sort by bitrate descending
    audio_formats.sort(key=lambda x: x.get('bitrate', 0), reverse=True)
    best = audio_formats[0]

    stream_url = best.get('url')
    if not stream_url:
        raise Exception('No direct URL (cipher protected)')

    # Ambil title dari videoDetails
    title = data.get('videoDetails', {}).get('title', video_id)
    author = data.get('videoDetails', {}).get('author', '')
    duration = int(data.get('videoDetails', {}).get('lengthSeconds', 0))
    thumbnail = ''
    thumbs = data.get('videoDetails', {}).get('thumbnail', {}).get('thumbnails', [])
    if thumbs:
        thumbnail = thumbs[-1]['url']

    return {
        'url': stream_url,
        'title': title,
        'artist': author,
        'duration': duration,
        'thumbnail': thumbnail,
        'mimeType': best.get('mimeType', 'audio/mp4'),
        'bitrate': best.get('bitrate', 0),
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
        from urllib.parse import urlparse, parse_qs
        params = parse_qs(urlparse(self.path).query)
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
