import re
import json
import requests
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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
}

def search_youtube(query: str, limit: int = 10):
    url = f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}&sp=EgIQAQ%253D%253D"
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        match = re.search(r'var ytInitialData = ({.*?});</script>', r.text, re.DOTALL)
        if not match:
            return []
        data = json.loads(match.group(1))
        contents = (
            data.get("contents", {})
            .get("twoColumnSearchResultsRenderer", {})
            .get("primaryContents", {})
            .get("sectionListRenderer", {})
            .get("contents", [])
        )
        results = []
        for section in contents:
            items = section.get("itemSectionRenderer", {}).get("contents", [])
            for item in items:
                v = item.get("videoRenderer")
                if not v:
                    continue
                video_id = v.get("videoId", "")
                title = v.get("title", {}).get("runs", [{}])[0].get("text", "Unknown")
                artist = "Unknown"
                for line in v.get("longBylineText", {}).get("runs", []):
                    artist = line.get("text", "Unknown")
                    break
                thumbs = v.get("thumbnail", {}).get("thumbnails", [])
                thumb = thumbs[-1]["url"] if thumbs else ""
                if video_id:
                    results.append({
                        "videoId": video_id,
                        "title": title,
                        "artist": artist,
                        "thumbnail": thumb
                    })
                if len(results) >= limit:
                    break
            if len(results) >= limit:
                break
        return results
    except Exception as e:
        return []

@app.get("/api/search")
def search_music(query: str, limit: int = 10):
    try:
        results = search_youtube(query, limit)
        return {"status": "success", "data": results}
    except Exception as e:
        return {"status": "error", "message": str(e), "data": []}

@app.get("/api/lyrics")
def get_lyrics(video_id: str):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        r = requests.get(url, headers=HEADERS, timeout=8)
        title_match = re.search(r'"title":"([^"]+)"', r.text)
        title = title_match.group(1) if title_match else "Unknown"
        return {
            "status": "success",
            "data": {
                "lyrics": f'<div style="color:rgba(255,255,255,0.85);font-size:16px;line-height:2;text-align:center;padding:20px 0;">Lirik untuk <b>{title}</b><br><br><span style="color:rgba(255,255,255,0.5);font-size:14px;">Cari lirik di Google: <a href="https://www.google.com/search?q={requests.utils.quote(title)}+lirik" target="_blank" style="color:#1ed760;">klik di sini</a></span></div>'
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

handler = Mangum(app)
