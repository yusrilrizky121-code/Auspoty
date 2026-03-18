with open('public/script.js', 'rb') as f:
    d = f.read()
i = d.find(b'// PROFILE PHOTO')
print(repr(d[i:i+400]))
