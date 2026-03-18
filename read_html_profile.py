with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Edit profile modal
i = html.find('editProfileModal')
print("=== editProfileModal ===")
print(repr(html[i:i+800]))

# Firebase imports
i2 = html.find('firebase-firestore')
print("\n=== Firestore import ===")
print(repr(html[i2-50:i2+400]))

# profilePhotoInput
i3 = html.find('profilePhotoInput')
print("\n=== profilePhotoInput ===")
print(repr(html[i3-50:i3+200]))
