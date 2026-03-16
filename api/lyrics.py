import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        video_id = params.get('video_id', [''])[0]

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        if not video_id:
            self.wfile.write(json.dumps({"status": "error", "message": "video_id required"}).encode())
            return

        try:
            from ytmusicapi import YTMusic
            yt = YTMusic()
            watch = yt.get_watch_playlist(videoId=video_id)
            lyrics_id = watch.get("lyrics")
            if not lyrics_id:
                self.wfile.write(json.dumps({"status": "error", "message": "Lirik tidak ditemukan"}).encode())
                return
            lyrics = yt.get_lyrics(lyrics_id)
            self.wfile.write(json.dumps({"status": "success", "data": lyrics}).encode())
        except Exception as e:
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
