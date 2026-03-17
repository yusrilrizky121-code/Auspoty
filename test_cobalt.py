import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

instances = [
    "https://cobalt-api.meowing.de",
    "https://capi.3kh0.net",
    "https://cobalt-backend.canine.tools",
]

payload = json.dumps({
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "downloadMode": "audio",
    "audioFormat": "mp3",
    "audioBitrate": "128",
    "filenameStyle": "basic"
}).encode()

for inst in instances:
    try:
        req = urllib.request.Request(
            inst + "/",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Auspoty/1.0 (+https://github.com/test)"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            body = r.read()
            result = json.loads(body)
            print(f"\nOK {inst}")
            print("  status:", result.get("status"))
            print("  url:", str(result.get("url",""))[:80])
            print("  error:", result.get("error"))
    except Exception as e:
        print(f"\nFAIL {inst}: {e}")
