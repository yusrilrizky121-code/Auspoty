import re, os

base = r'C:\Users\Admin\Downloads\Auspoty'
js_path = os.path.join(base, 'public', 'script.js')

with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Tulis ulang openEditProfile bersih
old = re.search(r'function openEditProfile\(\)\s*\{.*?\n\}', content, re.DOTALL)
if old:
    new_fn = """function openEditProfile() {
    var s = getSettings();
    var user = getGoogleUser();
    var nameInput = document.getElementById('editProfileName');
    if (nameInput) nameInput.value = s.profileName || (user ? user.name : '');
    var av = document.getElementById('editProfileAvatar');
    var customPhoto = localStorage.getItem('auspotyCustomPhoto');
    if (av) {
        var photoSrc = customPhoto || (user ? user.picture : null);
        if (photoSrc) {
            av.innerHTML = '<img src="' + photoSrc + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">';
        } else {
            av.innerHTML = '';
            av.innerText = (s.profileName || 'A').charAt(0).toUpperCase();
        }
    }
    var modal = document.getElementById('editProfileModal');
    if (modal) { modal.style.display = 'flex'; }
}"""
    content = content[:old.start()] + new_fn + content[old.end():]
    print("openEditProfile OK")
else:
    print("openEditProfile TIDAK DITEMUKAN")

# Tulis ulang previewProfilePhoto bersih
old2 = re.search(r'function previewProfilePhoto\(event\)\s*\{.*?\n\}', content, re.DOTALL)
if old2:
    new_fn2 = """function previewProfilePhoto(event) {
    var file = event.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function(e) {
        var dataUrl = e.target.result;
        localStorage.setItem('auspotyCustomPhoto', dataUrl);
        var av = document.getElementById('editProfileAvatar');
        if (av) av.innerHTML = '<img src="' + dataUrl + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">';
        updateProfileUI();
        showToast('Foto profil diperbarui!');
    };
    reader.readAsDataURL(file);
}"""
    content = content[:old2.start()] + new_fn2 + content[old2.end():]
    print("previewProfilePhoto OK")
else:
    print("previewProfilePhoto TIDAK DITEMUKAN")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SELESAI")
