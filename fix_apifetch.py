JS_PATH = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

print('Before - fetch /api/ count:', js.count("fetch('/api/"))
print('Before - apiFetch count:', js.count('apiFetch('))

# Ganti semua fetch('/api/ dengan apiFetch('/api/
js = js.replace("fetch('/api/", "apiFetch('/api/")

print('After - fetch /api/ count:', js.count("fetch('/api/"))
print('After - apiFetch count:', js.count('apiFetch('))

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

print('Saved.')
