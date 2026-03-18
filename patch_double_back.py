with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari popstate handler yang sudah ada
old_pop = """// Handle tombol back browser/Android WebView
window.addEventListener('popstate', function(e) {
    if (e.state && e.state.view) {
        // Navigasi ke view sebelumnya tanpa push state baru
        document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
        const target = document.getElementById('view-' + e.state.view);
        if (target) target.classList.add('active');
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        const navMap = { home: 0, search: 1, library: 2, settings: 3 };
        const navItems = document.querySelectorAll('.nav-item');
        if (navMap[e.state.view] !== undefined && navItems[navMap[e.state.view]]) {
            navItems[navMap[e.state.view]].classList.add('active');
        }
        window.scrollTo(0, 0);
    } else {
        // Tidak ada state — kembali ke home
        document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
        const home = document.getElementById('view-home');
        if (home) home.classList.add('active');
        const navItems = document.querySelectorAll('.nav-item');
        if (navItems[0]) navItems[0].classList.add('active');
    }
});"""

new_pop = """// Handle tombol back browser/Android WebView
var _lastBackTime = 0;
var _backToast = null;

function _showBackToast() {
    var existing = document.getElementById('backExitToast');
    if (existing) { existing.remove(); }
    var t = document.createElement('div');
    t.id = 'backExitToast';
    t.innerText = 'Tekan sekali lagi untuk keluar';
    t.style.cssText = 'position:fixed;bottom:90px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.85);color:white;padding:10px 20px;border-radius:20px;font-size:13px;z-index:99999;pointer-events:none;transition:opacity 0.3s;';
    document.body.appendChild(t);
    setTimeout(function() { if (t.parentNode) { t.style.opacity='0'; setTimeout(function(){ if(t.parentNode) t.remove(); }, 300); } }, 2000);
}

window.addEventListener('popstate', function(e) {
    if (e.state && e.state.view && e.state.view !== 'home') {
        // Navigasi ke view sebelumnya tanpa push state baru
        document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
        const target = document.getElementById('view-' + e.state.view);
        if (target) target.classList.add('active');
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        const navMap = { home: 0, search: 1, library: 2, settings: 3 };
        const navItems = document.querySelectorAll('.nav-item');
        if (navMap[e.state.view] !== undefined && navItems[navMap[e.state.view]]) {
            navItems[navMap[e.state.view]].classList.add('active');
        }
        window.scrollTo(0, 0);
        // Push ulang agar ada entry untuk back berikutnya
        window.history.pushState({ view: e.state.view }, '', '#' + e.state.view);
    } else {
        // Sudah di home — double back to exit
        var now = Date.now();
        if (now - _lastBackTime < 2000) {
            // Tekan 2x — biarkan browser keluar secara normal
            return;
        }
        _lastBackTime = now;
        _showBackToast();
        // Push state home lagi agar tidak langsung keluar
        window.history.pushState({ view: 'home' }, '', '#home');
    }
});"""

if old_pop in content:
    content = content.replace(old_pop, new_pop)
    print("OK: popstate double-back added")
else:
    print("WARN: popstate pattern not found, searching...")
    i = content.find('window.addEventListener(\'popstate\'')
    if i < 0:
        i = content.find('window.addEventListener("popstate"')
    print(repr(content[i:i+100]) if i >= 0 else "NOT FOUND")

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
