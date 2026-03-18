import urllib.request, json
url = 'https://clone2-git-master-yusrilrizky121-codes-projects.vercel.app/api/search?query=lagu+indonesia+terbaru+2025'
try:
    r = urllib.request.urlopen(url, timeout=10)
    data = json.loads(r.read())
    print('Status:', data.get('status'))
    print('Count:', len(data.get('data', [])))
    if data.get('data'):
        print('First:', data['data'][0].get('title'))
except Exception as e:
    print('ERROR:', e)
