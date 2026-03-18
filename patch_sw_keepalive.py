with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

sw_ping = """
// Service Worker keep-alive ping — cegah SW di-terminate browser saat background
(function() {
    function pingSW() {
        if (!navigator.serviceWorker || !navigator.serviceWorker.controller) return;
        var mc = new MessageChannel();
        navigator.serviceWorker.controller.postMessage({ type: 'KEEP_ALIVE' }, [mc.port2]);
    }
    // Ping setiap 20 detik saat musik sedang main
    setInterval(function() {
        if (typeof isPlaying !== 'undefined' && isPlaying) pingSW();
    }, 20000);
})();

"""

# Sisipkan setelah blok background audio keep-alive
marker = "})();\n\n// ============================================================\n// BACKGROUND AUDIO KEEP-ALIVE"
# Cari akhir dari blok background audio
end_marker = "})();\n\n"
# Sisipkan sebelum // INDEXEDDB
insert_before = "// INDEXEDDB"
if insert_before in content:
    content = content.replace(insert_before, sw_ping + insert_before, 1)
    print("OK: SW keep-alive ping added")
else:
    print("WARN: INDEXEDDB marker not found")

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
