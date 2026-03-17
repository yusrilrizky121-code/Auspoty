import subprocess, sys

# Test apakah yt-dlp bisa diinstall dan dijalankan
result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "yt-dlp", "--quiet"],
    capture_output=True, text=True
)
print("pip install:", result.returncode, result.stderr[:100] if result.stderr else "OK")

# Test yt-dlp get info
result2 = subprocess.run(
    [sys.executable, "-m", "yt_dlp", "--get-url", "--format", "bestaudio",
     "--no-playlist", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
    capture_output=True, text=True, timeout=30
)
print("yt-dlp returncode:", result2.returncode)
print("stdout:", result2.stdout[:200])
print("stderr:", result2.stderr[:200])
