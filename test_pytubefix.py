import subprocess, sys

# Install pytubefix
r = subprocess.run([sys.executable, "-m", "pip", "install", "pytubefix", "-q"],
    capture_output=True, text=True, timeout=30)
print("install:", r.returncode, r.stderr[:80] if r.stderr else "OK")

# Test get audio stream URL
try:
    from pytubefix import YouTube
    yt = YouTube("https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                 use_oauth=False, allow_oauth_cache=False)
    stream = yt.streams.filter(only_audio=True).order_by('abr').last()
    print("title:", yt.title)
    print("stream:", stream)
    print("url:", stream.url[:80] if stream else "None")
except Exception as e:
    print("ERROR:", e)
