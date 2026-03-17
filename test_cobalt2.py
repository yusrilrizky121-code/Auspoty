import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

inst = "https://cobalt-api.meowing.de"

# Test 1: cek GET / dulu untuk lihat versi
try:
    req = urllib.request.Request(inst + "/", headers={"Accept": "application/json", "User-Agent": "test/1.0"})
    with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
        print("GET / status:", r.status)
        print("GET / body:", r.read().decode()[:300])
except urllib.error.HTTPError as e:
    print("GET / error:", e.code, e.read().decode()[:300])
except Exception as e:
    print("GET / fail:", e)

print()

# Test 2: POST dengan format minimal
payload = json.dumps({"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}).encode()
try:
    req = urllib.request.Request(
        inst + "/",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "test/1.0"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        body = r.read().decode()
        print("POST minimal OK:", body[:300])
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print("POST minimal error", e.code, ":", body[:300])
except Exception as e:
    print("POST minimal fail:", e)
