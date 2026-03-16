import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy init supaya cold start tidak timeout
_ytmusic = None

def get_ytmusic():
    global _ytmusic
    if _ytmusic is None:
        from ytmusicapi import YTMusic
        _ytmusic = YTMusic()
    return _ytmusic

def format_results(search_results):
    cleaned = []
    for item in search_results:
        if 'videoId' in item:
            cleaned.append({
                "videoId": item['videoId'],
                "title": item.get('title', 'Unknown Title'),
                "artist": item.get('artists', [{'name': 'Unknown Artist'}])[0]['name'] if item.get('artists') else 'Unknown Artist',
                "thumbnail": item['thumbnails'][-1]['url'] if item.get('thumbnails') else ''
            })
    return cleaned

@app.get("/api/test")
def test():
    return {"status": "ok", "python": sys.version, "path": sys.path[:3]}

@app.get("/api/search")
def search_music(query: str):
    try:
        yt = get_ytmusic()
        results = yt.search(query, filter="songs", limit=12)
        data = format_results(results)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e), "data": []}

@app.get("/api/lyrics")
def get_lyrics(video_id: str):
    try:
        yt = get_ytmusic()
        watch = yt.get_watch_playlist(videoId=video_id)
        lyrics_id = watch.get("lyrics")
        if not lyrics_id:
            return {"status": "error", "message": "Lirik tidak ditemukan"}
        lyrics = yt.get_lyrics(lyrics_id)
        return {"status": "success", "data": lyrics}
    except Exception as e:
        return {"status": "error", "message": str(e)}

handler = Mangum(app)
