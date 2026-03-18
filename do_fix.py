p = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
js = open(p,'r',encoding='utf-8').read()

# Tambah apiFetch function setelah REPEAT & HISTORY block
apifetch_fn = '''
// API FETCH dengan fallback ke deployment aktif
async function apiFetch(path) {
    const FALLBACK = 'https://clone2-git-master-yusrilrizky121-codes-projects.vercel.app';
    try {
        const r = await fetch(path);
        if (r.ok) return r;
        throw new Error('not ok');
    } catch(e) {
        return fetch(FALLBACK + path);
    }
}
'''

# Insert setelah "let songHistory = [];"
marker = 'let songHistory = [];'
if marker in js:
    js = js.replace(marker, marker + apifetch_fn, 1)
    print('apiFetch inserted')
else:
    print('ERROR: marker not found')

# Ganti semua fetch('/api/ dengan apiFetch('/api/
before = js.count("fetch('/api/")
js = js.replace("fetch('/api/", "apiFetch('/api/")
after = js.count("fetch('/api/")
print(f'Replaced {before-after} fetch calls, apiFetch count: {js.count("apiFetch(")}')

open(p,'w',encoding='utf-8').write(js)
print('Saved.')
