import urllib.request, json, time, random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120',
    'Referer': 'https://id.ytmp3.mobi/v1/',
    'Origin': 'https://id.ytmp3.mobi',
}

def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    r = urllib.request.urlopen(req, timeout=15)
    return json.loads(r.read().decode())

video_id = 'dQw4w9WgXcQ'

# Step 1: init
rnd = random.random()
init_url = f'https://a.ymcdn.org/api/v1/init?p=y&23=1llum1n471&_={rnd}'
print('Step 1 - init:', init_url)
d = get(init_url)
print('Init response:', json.dumps(d, indent=2)[:300])

if d.get('error', 0) > 0:
    print('ERROR:', d)
    exit()

convert_url = d.get('convertURL', '')
print('\nconvertURL:', convert_url)

# Step 2: convert
rnd2 = random.random()
conv_full = f'{convert_url}&v={video_id}&f=mp3&_={rnd2}'
print('\nStep 2 - convert:', conv_full)
d2 = get(conv_full)
print('Convert response:', json.dumps(d2, indent=2)[:300])

progress_url = d2.get('progressURL', '')
download_url = d2.get('downloadURL', '')
print('\nprogressURL:', progress_url)
print('downloadURL:', download_url)

# Step 3: poll progress
for i in range(30):
    time.sleep(1)
    rnd3 = random.random()
    d3 = get(f'{progress_url}&_={rnd3}')
    prog = d3.get('progress', 0)
    print(f'  Progress {i+1}: {prog} - {d3}')
    if prog >= 3:
        final_url = d3.get('downloadURL') or download_url
        print('\nFINAL DOWNLOAD URL:', final_url)
        break
