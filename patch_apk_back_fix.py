with open('auspoty-apk/app/src/main/java/com/auspoty/app/MainActivity.java', 'r', encoding='utf-8') as f:
    java = f.read()

# Ganti onKeyDown — hapus webView.canGoBack() check
# karena kita manage history sendiri via JS pushState
old_keydown = '''    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            // Coba navigasi balik di WebView dulu (jika ada history internal)
            if (webView.canGoBack()) {
                webView.goBack();
                return true;
            }
            // Cek view aktif via JS
            webView.evaluateJavascript(
                "(function(){ " +
                "  var active = document.querySelector('.view-section.active');" +
                "  return active ? active.id : 'view-home';" +
                "})()",
                result -> {
                    if (result == null) result = "\\"view-home\\"";
                    // Hapus tanda kutip dari hasil JS
                    final String viewId = result.replace("\\"", "").trim();

                    // Cek apakah ini view yang trigger double-back
                    boolean isDoubleBackView = false;
                    for (String v : DOUBLE_BACK_VIEWS) {
                        if (v.equals(viewId)) { isDoubleBackView = true; break; }
                    }

                    if (isDoubleBackView) {
                        // Di home/search/library — double back to exit
                        long now = System.currentTimeMillis();
                        if (now - lastBackPressTime < 2000) {
                            // Tekan 2x → minimize app (bukan kill)
                            runOnUiThread(() -> moveTaskToBack(true));
                        } else {
                            lastBackPressTime = now;
                            runOnUiThread(() ->
                                android.widget.Toast.makeText(
                                    MainActivity.this,
                                    "Tekan sekali lagi untuk keluar",
                                    android.widget.Toast.LENGTH_SHORT
                                ).show()
                            );
                        }
                    } else {
                        // Di settings atau view sub → kembali ke home
                        runOnUiThread(() ->
                            webView.evaluateJavascript(
                                "if(typeof switchView==='function') switchView('home');", null)
                        );
                    }
                }
            );
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }'''

new_keydown = '''    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            // JANGAN pakai webView.canGoBack() — kita manage history sendiri via JS pushState
            // Langsung cek view aktif via JS
            webView.evaluateJavascript(
                "(function(){ " +
                "  var active = document.querySelector('.view-section.active');" +
                "  return active ? active.id : 'view-home';" +
                "})()",
                result -> {
                    if (result == null) result = "\\"view-home\\"";
                    final String viewId = result.replace("\\"", "").trim();

                    // home/search/library → double back to exit
                    boolean isDoubleBackView = false;
                    for (String v : DOUBLE_BACK_VIEWS) {
                        if (v.equals(viewId)) { isDoubleBackView = true; break; }
                    }

                    if (isDoubleBackView) {
                        long now = System.currentTimeMillis();
                        if (now - lastBackPressTime < 2000) {
                            // Tekan 2x dalam 2 detik → minimize app
                            runOnUiThread(() -> moveTaskToBack(true));
                        } else {
                            lastBackPressTime = now;
                            runOnUiThread(() ->
                                android.widget.Toast.makeText(
                                    MainActivity.this,
                                    "Tekan sekali lagi untuk keluar",
                                    android.widget.Toast.LENGTH_SHORT
                                ).show()
                            );
                        }
                    } else {
                        // settings atau view sub → kembali ke home
                        runOnUiThread(() ->
                            webView.evaluateJavascript(
                                "if(typeof switchView==='function') switchView('home');", null)
                        );
                    }
                }
            );
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }'''

if old_keydown in java:
    java = java.replace(old_keydown, new_keydown)
    print('OK: onKeyDown fixed - removed canGoBack() check')
else:
    print('WARN: exact match not found, trying to remove canGoBack block only...')
    old_cangback = '''            // Coba navigasi balik di WebView dulu (jika ada history internal)
            if (webView.canGoBack()) {
                webView.goBack();
                return true;
            }
            // Cek view aktif via JS'''
    new_cangback = '''            // Langsung cek view aktif via JS (tidak pakai canGoBack karena history dikelola JS)'''
    if old_cangback in java:
        java = java.replace(old_cangback, new_cangback)
        print('OK: canGoBack removed')
    else:
        print('ERROR: could not patch')

with open('auspoty-apk/app/src/main/java/com/auspoty/app/MainActivity.java', 'w', encoding='utf-8') as f:
    f.write(java)
print('MainActivity.java saved.')
print('DONE.')
