path = r'C:\Users\Admin\Downloads\Auspoty\auspoty-flutter\lib\main.dart'
content = open(path, 'r', encoding='utf-8').read()

# FIX 2: Tambah openGoogleLogin handler setelah openDownload handler
old_dl_handler = '''                  controller.addJavaScriptHandler(
                    handlerName: 'openDownload',
                    callback: (args) async {
                      final url = args.isNotEmpty ? args[0].toString() : '';
                      if (url.isNotEmpty) {
                        await launchUrl(Uri.parse(url),
                            mode: LaunchMode.externalApplication);
                      }
                    },
                  );'''

new_dl_handler = '''                  controller.addJavaScriptHandler(
                    handlerName: 'openDownload',
                    callback: (args) async {
                      final url = args.isNotEmpty ? args[0].toString() : '';
                      if (url.isNotEmpty) {
                        final uri = Uri.parse(url);
                        if (await canLaunchUrl(uri)) {
                          await launchUrl(uri, mode: LaunchMode.externalApplication);
                        }
                      }
                    },
                  );
                  controller.addJavaScriptHandler(
                    handlerName: 'openGoogleLogin',
                    callback: (args) async {
                      // Buka halaman login.html di Chrome eksternal
                      // Chrome bisa handle Google popup — tidak diblokir
                      const loginUrl = 'https://clone2-git-master-yusrilrizky121-codes-projects.vercel.app/login.html';
                      final uri = Uri.parse(loginUrl);
                      if (await canLaunchUrl(uri)) {
                        await launchUrl(uri, mode: LaunchMode.externalApplication);
                      }
                    },
                  );'''

if old_dl_handler in content:
    content = content.replace(old_dl_handler, new_dl_handler, 1)
    print('Fix 2 OK: openGoogleLogin handler added')
else:
    print('Fix 2 FAIL: openDownload handler pattern not found')
    idx = content.find('openDownload')
    print(repr(content[idx-50:idx+300]))

# FIX 3: Tambah onCreateWindow untuk handle popup Google login di dalam WebView
# Ini penting supaya signInWithPopup bisa buka window baru
old_load_stop = '''                onLoadStop: (controller, url) async {
                  setState(() => _isLoading = false);
                  await _injectAll(controller);
                },'''

new_load_stop = '''                onLoadStop: (controller, url) async {
                  setState(() => _isLoading = false);
                  final urlStr = url?.toString() ?? '';
                  if (urlStr.contains('vercel.app') || urlStr.contains('clone2') || urlStr.isEmpty || urlStr == 'about:blank') {
                    await _injectAll(controller);
                  }
                },
                onCreateWindow: (controller, createWindowAction) async {
                  // Handle popup window dari signInWithPopup Firebase
                  // Buka di browser eksternal supaya Google tidak block
                  final url = createWindowAction.request.url?.toString() ?? '';
                  if (url.isNotEmpty && url != 'about:blank') {
                    final uri = Uri.parse(url);
                    if (await canLaunchUrl(uri)) {
                      await launchUrl(uri, mode: LaunchMode.externalApplication);
                    }
                  }
                  return true;
                },'''

if old_load_stop in content:
    content = content.replace(old_load_stop, new_load_stop, 1)
    print('Fix 3 OK: onCreateWindow added')
else:
    print('Fix 3 FAIL: onLoadStop pattern not found')
    idx = content.find('onLoadStop')
    print(repr(content[idx:idx+200]))

open(path, 'w', encoding='utf-8').write(content)
print('Saved!')

# Verify
content2 = open(path, 'r', encoding='utf-8').read()
print(f"\nVerification:")
print(f"  openGoogleLogin handler: {'openGoogleLogin' in content2}")
print(f"  onCreateWindow: {'onCreateWindow' in content2}")
print(f"  thirdPartyCookiesEnabled: {'thirdPartyCookiesEnabled' in content2}")
