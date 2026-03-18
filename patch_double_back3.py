import re

# ============================================================
# PATCH: Double back to exit di semua view utama (home/search/library)
# Jangan di settings — settings tetap kembali ke home
# ============================================================

# --- FIX script.js ---
with open('public/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Ganti seluruh blok popstate handler + init state
old_popstate = '''window.addEventListener('popstate', function(e) {
    // Semua view utama (home/search/library/settings) → double back to exit
    // View sub (artist, playlist, developer) → kembali ke home
    var mainViews = ['home', 'search', 'library', 'settings'];
    var currentView = (e.state && e.state.view) ? e.state.view : 'home';

    if (mainViews.indexOf(currentView) >= 0) {
        // Di view utama — double back
        var now = Date.now();
        if (now - _lastBackTime < 2000) {
            // Tekan 2x — biarkan browser keluar
            return;
        }
        _lastBackTime = now;
        _showBackToast();
        // Push state ulang agar tidak langsung keluar
        window.history.pushState({ view: currentView }, '', '#' + currentView);
    } else {
        // Di view sub — kembali ke home
        document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
        var home = document.getElementById('view-home');
        if (home) home.classList.add('active');
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        var navItems = document.querySelectorAll('.nav-item');
        if (navItems[0]) navItems[0].classList.add('active');
        window.scrollTo(0, 0);
        window.history.pushState({ view: 'home' }, '', '#home');
    }
});

// Push state awal saat halaman load agar ada entry di history
(function() {
    if (window.history && window.history.replaceState) {
        window.history.replaceState({ view: 'home' }, '', '#home');
    }
})();'''

new_popstate = '''window.addEventListener('popstate', function(e) {
    // home/search/library → double back to exit
    // settings → kembali ke home (bukan exit)
    // View sub (artist, playlist, developer) → kembali ke home
    var doubleBackViews = ['home', 'search', 'library'];
    var currentView = (e.state && e.state.view) ? e.state.view : 'home';

    if (doubleBackViews.indexOf(currentView) >= 0) {
        // Di view utama — double back to exit
        var now = Date.now();
        if (now - _lastBackTime < 2000) {
            // Tekan 2x dalam 2 detik — keluar dari app
            return; // biarkan browser/WebView keluar
        }
        _lastBackTime = now;
        _showBackToast();
        // Push state ulang agar tidak langsung keluar
        window.history.pushState({ view: currentView }, '', '#' + currentView);
    } else if (currentView === 'settings') {
        // Di settings — kembali ke home, bukan exit
        document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
        var home = document.getElementById('view-home');
        if (home) home.classList.add('active');
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        var navItems = document.querySelectorAll('.nav-item');
        if (navItems[0]) navItems[0].classList.add('active');
        window.scrollTo(0, 0);
        window.history.pushState({ view: 'home' }, '', '#home');
    } else {
        // Di view sub (artist/playlist/developer) — kembali ke home
        document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
        var home2 = document.getElementById('view-home');
        if (home2) home2.classList.add('active');
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        var navItems2 = document.querySelectorAll('.nav-item');
        if (navItems2[0]) navItems2[0].classList.add('active');
        window.scrollTo(0, 0);
        window.history.pushState({ view: 'home' }, '', '#home');
    }
});

// Push state awal saat halaman load agar ada entry di history
(function() {
    if (window.history && window.history.replaceState) {
        window.history.replaceState({ view: 'home' }, '', '#home');
    }
    // Tambah satu entry lagi agar ada "sesuatu" untuk di-pop sebelum keluar
    if (window.history && window.history.pushState) {
        window.history.pushState({ view: 'home' }, '', '#home');
    }
})();'''

if old_popstate in js:
    js = js.replace(old_popstate, new_popstate)
    print('OK: popstate handler updated in script.js')
else:
    print('WARN: popstate block not found exactly, trying partial match...')
    # Coba ganti hanya bagian mainViews
    js = js.replace(
        "var mainViews = ['home', 'search', 'library', 'settings'];",
        "var doubleBackViews = ['home', 'search', 'library'];"
    )
    js = js.replace(
        "if (mainViews.indexOf(currentView) >= 0) {",
        "if (doubleBackViews.indexOf(currentView) >= 0) {"
    )
    print('OK: partial patch applied')

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('script.js saved.')

# --- FIX MainActivity.java ---
with open('auspoty-apk/app/src/main/java/com/auspoty/app/MainActivity.java', 'r', encoding='utf-8') as f:
    java = f.read()

old_onkeydown = '''    private long lastBackPressTime = 0;

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            // Coba navigasi balik di WebView dulu
            if (webView.canGoBack()) {
                webView.goBack();
                return true;
            }
            // Coba navigasi ke home via JS (jika bukan di home)
            webView.evaluateJavascript(
                "(function(){ " +
                "  var active = document.querySelector('.view-section.active');" +
                "  if (active && active.id !== 'view-home') {" +
                "    if (typeof switchView === 'function') switchView('home');" +
                "    return 'navigated';" +
                "  }" +
                "  return 'home';" +
                "})()",
                result -> {
                    if (result != null && result.contains("navigated")) {
                        // sudah navigasi ke home, jangan keluar
                    } else {
                        // Sudah di home — double back to exit
                        long now = System.currentTimeMillis();
                        if (now - lastBackPressTime < 2000) {
                            // Tekan back 2x dalam 2 detik → minimize
                            moveTaskToBack(true);
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
                    }
                }
            );
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }'''

new_onkeydown = '''    private long lastBackPressTime = 0;

    // View utama yang trigger double-back (home, search, library)
    // Settings → kembali ke home, bukan exit
    private static final String[] DOUBLE_BACK_VIEWS = {"view-home", "view-search", "view-library"};

    @Override
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
                    if (result == null) result = "\"view-home\"";
                    // Hapus tanda kutip dari hasil JS
                    final String viewId = result.replace("\"", "").trim();

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

if old_onkeydown in java:
    java = java.replace(old_onkeydown, new_onkeydown)
    print('OK: onKeyDown updated in MainActivity.java')
else:
    print('WARN: onKeyDown block not found exactly')
    # Coba cari dan ganti bagian kritis saja
    old_check = '''            // Coba navigasi ke home via JS (jika bukan di home)
            webView.evaluateJavascript(
                "(function(){ " +
                "  var active = document.querySelector('.view-section.active');" +
                "  if (active && active.id !== 'view-home') {" +
                "    if (typeof switchView === 'function') switchView('home');" +
                "    return 'navigated';" +
                "  }" +
                "  return 'home';" +
                "})()",
                result -> {
                    if (result != null && result.contains("navigated")) {
                        // sudah navigasi ke home, jangan keluar
                    } else {
                        // Sudah di home — double back to exit
                        long now = System.currentTimeMillis();
                        if (now - lastBackPressTime < 2000) {
                            // Tekan back 2x dalam 2 detik → minimize
                            moveTaskToBack(true);
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
                    }
                }
            );'''
    new_check = '''            // Cek view aktif via JS
            webView.evaluateJavascript(
                "(function(){ " +
                "  var active = document.querySelector('.view-section.active');" +
                "  return active ? active.id : 'view-home';" +
                "})()",
                result -> {
                    if (result == null) result = "\\"view-home\\"";
                    final String viewId = result.replace("\\"", "").trim();
                    // home/search/library → double back; settings/sub → ke home
                    boolean isDoubleBack = viewId.equals("view-home") || viewId.equals("view-search") || viewId.equals("view-library");
                    if (isDoubleBack) {
                        long now = System.currentTimeMillis();
                        if (now - lastBackPressTime < 2000) {
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
                        runOnUiThread(() ->
                            webView.evaluateJavascript(
                                "if(typeof switchView==='function') switchView('home');", null)
                        );
                    }
                }
            );'''
    if old_check in java:
        java = java.replace(old_check, new_check)
        print('OK: partial onKeyDown patch applied')
    else:
        print('ERROR: could not find onKeyDown block to patch')

with open('auspoty-apk/app/src/main/java/com/auspoty/app/MainActivity.java', 'w', encoding='utf-8') as f:
    f.write(java)
print('MainActivity.java saved.')
print('DONE.')
