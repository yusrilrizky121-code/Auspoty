path = r'C:\Users\Admin\Downloads\Auspoty\auspoty-flutter\lib\main.dart'
content = open(path, 'r', encoding='utf-8').read()

print(f"File size: {len(content)}")
print(f"Lines: {content.count(chr(10))}")

# Cek versi file
if 'openGoogleLogin' in content:
    print("openGoogleLogin handler: FOUND")
else:
    print("openGoogleLogin handler: NOT FOUND")

if 'thirdPartyCookiesEnabled' in content:
    print("thirdPartyCookiesEnabled: FOUND")
else:
    print("thirdPartyCookiesEnabled: NOT FOUND")

# Cek userAgent
idx = content.find('userAgent')
if idx >= 0:
    line = content[:idx].count('\n') + 1
    print(f"userAgent at line {line}: {content[idx:idx+100]}")

# Cek initialSettings
idx2 = content.find('initialSettings')
line2 = content[:idx2].count('\n') + 1
print(f"initialSettings at line {line2}")
