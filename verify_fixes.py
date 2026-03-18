with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Verifikasi deleteComment
i = content.find('async function deleteComment')
print("=== deleteComment ===")
print(repr(content[i:i+400]))

# Verifikasi loadComments docs mapping (harus ada .id)
i2 = content.find('snap.docs.map')
print("\n=== loadComments docs map ===")
print(repr(content[i2:i2+100]))

# Verifikasi openEditProfile
i3 = content.find('function openEditProfile')
print("\n=== openEditProfile ===")
print(repr(content[i3:i3+400]))
