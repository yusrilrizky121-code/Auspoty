with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# profilePhotoInput input element
i = html.find('type="file" id="profilePhotoInput"')
print("=== profilePhotoInput input ===")
print(repr(html[i-20:i+200]))

# Firestore full import block
i2 = html.find('import { getFirestore')
print("\n=== Firestore full import ===")
print(repr(html[i2:i2+400]))
