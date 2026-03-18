with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Cari popstate handler yang ada
i = content.find("window.addEventListener('popstate'")
end = content.find("\n});", i) + 4
print("Found popstate at:", i, "to", end)
old_pop = content[i:end]
print(repr(old_pop[:100]))

new_pop = """window.addEventListener('popstate', function(e) {
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
});"""

content = content[:i] + new_pop + content[end:]
print("OK: popstate replaced")

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
