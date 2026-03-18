with open('public/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix 1: Saat double-back di web, jangan return kosong (yang bikin keluar)
# Ganti: return; // biarkan browser/WebView keluar
# Dengan: push state lagi + coba window.close() (di web biasanya tidak bisa, tapi tidak keluar)
old = '''        if (now - _lastBackTime < 2000) {
            // Tekan 2x dalam 2 detik — keluar dari app
            return; // biarkan browser/WebView keluar
        }'''

new = '''        if (now - _lastBackTime < 2000) {
            // Tekan 2x dalam 2 detik — coba tutup tab/minimize
            // Di web: coba window.close(), kalau gagal push state lagi (tidak bisa keluar)
            // Di APK: onKeyDown yang handle exit via moveTaskToBack
            try { window.close(); } catch(ex) {}
            // Kalau window.close() gagal (web biasa), push state lagi supaya tidak keluar
            window.history.pushState({ view: currentView }, '', '#' + currentView);
            return;
        }'''

if old in js:
    js = js.replace(old, new)
    print('OK: double-back exit logic fixed')
else:
    print('WARN: target not found, trying alternative...')
    # Coba cari versi lain
    old2 = "            return; // biarkan browser/WebView keluar"
    new2 = """            try { window.close(); } catch(ex) {}
            window.history.pushState({ view: currentView }, '', '#' + currentView);
            return;"""
    if old2 in js:
        js = js.replace(old2, new2)
        print('OK: partial fix applied')
    else:
        print('ERROR: could not find target')

# Fix 2: Init — push lebih banyak entry agar ada buffer yang cukup
old_init = '''// Push state awal saat halaman load agar ada entry di history
(function() {
    if (window.history && window.history.replaceState) {
        window.history.replaceState({ view: 'home' }, '', '#home');
    }
    // Tambah satu entry lagi agar ada "sesuatu" untuk di-pop sebelum keluar
    if (window.history && window.history.pushState) {
        window.history.pushState({ view: 'home' }, '', '#home');
    }
})();'''

new_init = '''// Push state awal saat halaman load agar ada entry di history
(function() {
    if (window.history && window.history.replaceState) {
        window.history.replaceState({ view: 'home' }, '', '#home');
    }
    // Push 2 entry buffer agar back pertama tidak langsung keluar
    if (window.history && window.history.pushState) {
        window.history.pushState({ view: 'home' }, '', '#home');
        window.history.pushState({ view: 'home' }, '', '#home');
    }
})();'''

if old_init in js:
    js = js.replace(old_init, new_init)
    print('OK: init state buffer increased to 2 entries')
else:
    print('WARN: init block not found exactly')

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('script.js saved.')
print('DONE.')
