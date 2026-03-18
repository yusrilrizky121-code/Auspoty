with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# openEditProfile
i = content.find('function openEditProfile')
print("=== openEditProfile ===")
print(repr(content[i:i+700]))

# previewProfilePhoto / handleProfilePhotoChange
i2 = content.find('previewProfilePhoto')
print("\n=== previewProfilePhoto ===")
print(repr(content[i2:i2+300]))

# saveProfile
i3 = content.find('function saveProfile')
print("\n=== saveProfile ===")
print(repr(content[i3:i3+300]))

# deleteComment
i4 = content.find('async function deleteComment')
print("\n=== deleteComment ===")
print(repr(content[i4:i4+600]))

# Firestore imports di HTML
with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
i5 = html.find('deleteDoc')
print("\n=== deleteDoc in HTML ===")
print(repr(html[i5-100:i5+200]) if i5 >= 0 else "NOT FOUND")

i6 = html.find('_fsDelete')
print("\n=== _fsDelete in HTML ===")
print(repr(html[i6-50:i6+100]) if i6 >= 0 else "NOT FOUND")
