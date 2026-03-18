with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Tambah history.pushState di switchView
# ============================================================
old_switch = """function switchView(name) {
    document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
    const target = document.getElementById('view-' + name);
    if (target) target.classList.add('active');
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const navMap = { home: 0, search: 1, library: 2, settings: 3 };
    const navItems = document.querySelectorAll('.nav-item');
    if (navMap[name] !== undefined && navItems[navMap[name]]) navItems[navMap[name]].classList.add('active');
    window.scrollTo(0, 0);
}"""

new_switch = """function switchView(name) {
    document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
    const target = document.getElementById('view-' + name);
    if (target) target.classList.add('active');
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const navMap = { home: 0, search: 1, library: 2, settings: 3 };
    const navItems = document.querySelectorAll('.nav-item');
    if (navMap[name] !== undefined && navItems[navMap[name]]) navItems[navMap[name]].classList.add('active');
    window.scrollTo(0, 0);
    // Push ke browser history agar tombol back tidak keluar dari app
    if (window.history && window.history.pushState) {
        window.history.pushState({ view: name }, '', '#' + name);
    }
}

// Handle tombol back browser/Android WebView
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
});

// Push state awal saat halaman load agar ada entry di history
(function() {
    if (window.history && window.history.replaceState) {
        window.history.replaceState({ view: 'home' }, '', '#home');
    }
})();"""

if old_switch in content:
    content = content.replace(old_switch, new_switch)
    print("OK: switchView + popstate handler added")
else:
    print("WARN: switchView pattern not found")
    i = content.find('function switchView')
    print(repr(content[i:i+200]))

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
