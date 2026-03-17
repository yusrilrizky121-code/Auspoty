import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Dari instances.cobalt.best - filter yang cors:true, online:true, youtube:true
# capi.3kh0.net tidak butuh auth berdasarkan data instances
instances_to_test = [
    "https://capi.3kh0.net",
    "https://cobalt-api.meowing.de",
]

# Cek GET dulu untuk lihat apakah ada turnstile
for inst in instances_to_test:
    print(f"\n=== {inst} ===")
    try:
        req = urllib.request.Request(inst + "/", headers={"Accept": "application/json", "User-Agent": "test/1.0"})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            body = json.loads(r.read())
            cobalt = body.get("cobalt", {})
            print("  version:", cobalt.get("version"))
            print("  turnstile:", "YES" if cobalt.get("turnstileSitekey") else "NO")
            print("  services sample:", list(cobalt.get("services", []))[:5])
    except urllib.error.HTTPError as e:
        print("  GET error:", e.code, e.read().decode()[:200])
    except Exception as e:
        print("  GET fail:", e)

# Test POST ke capi.3kh0.net
print("\n\n=== POST test to capi.3kh0.net ===")
payload = json.dumps({"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}).encode()
try:
    req = urllib.request.Request(
        "https://capi.3kh0.net/",
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": "test/1.0"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        print("OK:", r.read().decode()[:300])
except urllib.error.HTTPError as e:
    print("Error", e.code, ":", e.read().decode()[:300])
except Exception as e:
    print("Fail:", e)
