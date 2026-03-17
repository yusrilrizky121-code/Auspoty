import subprocess, sys

VIDEO_ID = "dQw4w9WgXcQ"
yt_url = f"https://www.youtube.com/watch?v={VIDEO_ID}"

# Test berbagai kombinasi extractor args untuk bypass bot check
tests = [
    # iOS client - bypass bot check
    ["--extractor-args", "youtube:player_client=ios"],
    # Android client
    ["--extractor-args", "youtube:player_client=android"],
    # TV embedded
    ["--extractor-args", "youtube:player_client=tv_embedded"],
    # mweb
    ["--extractor-args", "youtube:player_client=mweb"],
]

for args in tests:
    label = args[1] if len(args) > 1 else "default"
    cmd = [sys.executable, "-m", "yt_dlp",
           "--get-url", "--format", "bestaudio[ext=m4a]/bestaudio/best",
           "--no-playlist", "--no-warnings", "--quiet"] + args + [yt_url]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if r.returncode == 0 and r.stdout.strip():
            url = r.stdout.strip().split("\n")[0]
            print(f"OK [{label}]: {url[:80]}...")
        else:
            err = (r.stderr or "no output").strip()[:120]
            print(f"FAIL [{label}]: {err}")
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT [{label}]")
    except Exception as e:
        print(f"ERROR [{label}]: {e}")
