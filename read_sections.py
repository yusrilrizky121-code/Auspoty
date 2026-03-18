with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari openEditProfile
i = content.find('editProfileAvatar')
print("=== openEditProfile area ===")
# Cari fungsi openEditProfile
j = content.rfind('function openEditProfile', 0, i)
print(repr(content[j:j+800]))

print("\n=== loadComments area ===")
k = content.find('async function loadComments')
print(repr(content[k:k+1500]))

print("\n=== INIT area ===")
m = content.find('// INIT')
print(repr(content[m:m+200]))
