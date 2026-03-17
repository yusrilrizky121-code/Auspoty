import shutil, os

base = r"C:\Users\Admin\Downloads\Auspoty"
apk_assets = base + r"\auspoty-apk\app\src\main\assets"

# Sync index.html dan style.css ke APK
shutil.copy(base + r"\public\index.html", apk_assets + r"\index.html")
shutil.copy(base + r"\public\style.css",  apk_assets + r"\style.css")

# Sync script.js ke APK dengan API_BASE prefix
src = open(base + r"\public\script.js", encoding="utf-8").read()
api_base = 'var API_BASE = "https://clone2-iyrr-git-master-yusrilrizky121-codes-projects.vercel.app";\n'
apk_js = api_base + src.replace("fetch('/api/", "fetch(API_BASE + '/api/")
open(apk_assets + r"\script.js", "w", encoding="utf-8").write(apk_js)

print("Synced:")
for f in ["index.html", "style.css", "script.js"]:
    size = os.path.getsize(apk_assets + "\\" + f)
    print(f"  {f}: {size} bytes")
