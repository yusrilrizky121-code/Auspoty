path = r'C:\Users\Admin\Downloads\Auspoty\auspoty-flutter\lib\main.dart'
content = open(path, 'r', encoding='utf-8').read()

# FIX: Tambah openGoogleLogin handler
# Cari akhir dari openDownload handler, lalu insert setelahnya
# Pattern: setelah closing ');\n' dari openDownload handler

# Cari posisi setelah openDownload handler selesai
idx = content.find("handlerName: 'openDownload'")
if idx < 0:
    print("ERROR: openDownload not found")
    exit()

# Cari closing ');\n' setelah openDownload
end_idx = content.find('\n                  );', idx)
end_idx2 = content.find('\n                  );', end_idx + 1)  # closing dari addJavaScriptHandler
insert_pos = end_idx2 + len('\n                  );')

print(f"Insert position: {insert_pos}")
print(f"Context: {repr(content[insert_pos-50:insert_pos+100])}")

google_login_handler = '''
                  controller.addJavaScriptHandler(
                    handlerName: 'openGoogleLogin',
                    callback: (args) async {
                      // Buka login.html di Chrome — Chrome bisa handle Google popup
                      const loginUrl = 'https://clone2-git-master-yusrilrizky121-codes-projects.vercel.app/login.html';
                      final uri = Uri.parse(loginUrl);
                      if (await canLaunchUrl(uri)) {
                        await launchUrl(uri, mode: LaunchMode.externalApplication);
                      }
                    },
                  );'''

content = content[:insert_pos] + google_login_handler + content[insert_pos:]
print("openGoogleLogin handler inserted")

# FIX: Tambah onCreateWindow setelah onLoadStop
old_load = '''onLoadStop: (controller, url) async {
                  setState(() => _isLoading = false);
                  final urlStr = url?.toString() ?? '';
                  if (urlStr.contains('vercel.app') || urlStr.contains('clone2')) {
                    await _injectAll(controller);
                  }
                },'''

new_load = '''onLoadStop: (controller, url) async {
                  setState(() => _isLoading = false);
                  final urlStr = url?.toString() ?? '';
                  if (urlStr.contains('vercel.app') || urlStr.contains('clone2') || urlStr.isEmpty) {
                    await _injectAll(controller);
                  }
                },
                onCreateWindow: (controller, createWindowAction) async {
                  // Handle popup dari signInWithPopup Firebase
                  final url = createWindowAction.request.url?.toString() ?? '';
                  if (url.isNotEmpty && url != 'about:blank') {
                    final uri = Uri.parse(url);
                    if (await canLaunchUrl(uri)) {
                      await launchUrl(uri, mode: LaunchMode.externalApplication);
                    }
                  }
                  return true;
                },'''

if old_load in content:
    content = content.replace(old_load, new_load, 1)
    print("onCreateWindow added")
else:
    print("FAIL: onLoadStop pattern not found")
    idx2 = content.find('onLoadStop')
    print(repr(content[idx2:idx2+300]))

open(path, 'w', encoding='utf-8').write(content)
print("Saved!")

# Verify
c2 = open(path, 'r', encoding='utf-8').read()
print(f"\nVerification:")
print(f"  openGoogleLogin: {'openGoogleLogin' in c2}")
print(f"  onCreateWindow: {'onCreateWindow' in c2}")
print(f"  thirdPartyCookiesEnabled: {'thirdPartyCookiesEnabled' in c2}")
