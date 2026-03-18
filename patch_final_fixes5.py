with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Lihat konteks lengkap di sekitar d.name+badge
i = content.find("d.name+'</span>'+badge")
print(repr(content[i-100:i+300]))
