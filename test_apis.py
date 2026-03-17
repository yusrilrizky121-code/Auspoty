import urllib.request, json, ssl, urllib.parse

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

VIDEO_ID = "dQw4w9WgXcQ"

def get(url, headers=None):
    try:
        req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            return r.status, r.read().decode()[:300]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:200]
    except Exception as e:
        return 0, str(e)[:100]

# Test 1: ytjar API (ytmp3.cc backend)
print("=== ytjar (ytmp3.cc) ===")
code, body = get(f"https://ytjar.info/api/json?id={VIDEO_ID}&q=128")
print(code, body)

# Test 2: loader.to
print("\n=== loader.to ===")
code, body = get(f"https://loader.to/api/button/?url=https://www.youtube.com/watch?v={VIDEO_ID}&f=mp3")
print(code, body)

# Test 3: yt5s API
print("\n=== yt5s ===")
code, body = get(f"https://yt5s.ltd/api/ajaxSearch/index", {"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"})
print(code, body)

# Test 4: cnvmp3
print("\n=== cnvmp3 ===")
code, body = get(f"https://cnvmp3.com/v25/{VIDEO_ID}")
print(code, body)

# Test 5: y2mate API
print("\n=== y2mate analyze ===")
import urllib.request as ur
payload = urllib.parse.urlencode({"url": f"https://www.youtube.com/watch?v={VIDEO_ID}", "q_auto": "0", "ajax": "1"}).encode()
try:
    req = ur.Request("https://www.y2mate.com/mates/analyzeV2/ajax", data=payload,
        headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded",
                 "X-Requested-With": "XMLHttpRequest"})
    with ur.urlopen(req, timeout=10, context=ctx) as r:
        print(r.status, r.read().decode()[:300])
except Exception as e:
    print("fail:", e)
