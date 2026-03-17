import urllib.request, re

req = urllib.request.Request(
    'https://id.ytmp3.mobi/js/ytmp3.js?t=1770957289',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120'}
)
r = urllib.request.urlopen(req, timeout=10)
js = r.read().decode('utf-8', errors='ignore')

# Find verify function and API calls
# Look for fetch/XHR calls with URLs
xhr_urls = re.findall(r'open\(["\'](?:GET|POST)["\'],\s*["\']([^"\']+)["\']', js)
fetch_urls = re.findall(r'fetch\(["\']([^"\']+)["\']', js)
print('XHR URLs:', xhr_urls)
print('Fetch URLs:', fetch_urls)

# Find verify function
verify_match = re.search(r'function verify\s*\([^)]*\)\s*\{(.{0,1000})', js, re.DOTALL)
if verify_match:
    print('\nverify():', verify_match.group(0)[:800])

# Find convert/progress related
for pattern in ['convert', 'progress', 'download', 'p.php', 'c.php', 'v.php']:
    matches = [line.strip() for line in js.split(';') if pattern in line]
    if matches:
        print(f'\n{pattern}:', matches[:3])
