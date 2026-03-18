with open('public/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Sisipkan fungsi filterHome setelah applyLanguageTitles
filter_home_fn = """
// HOME PILLS FILTER — Semua / Musik / Podcast
const PODCAST_QUERIES = [
    { id: 'rowAnyar',   query: 'podcast indonesia terpopuler 2025' },
    { id: 'rowGembira', query: 'podcast motivasi inspirasi indonesia' },
    { id: 'rowCharts',  query: 'podcast trending indonesia 2025' },
    { id: 'rowGalau',   query: 'podcast cerita misteri indonesia' },
    { id: 'rowTiktok',  query: 'podcast viral indonesia 2025' },
    { id: 'rowHits',    query: 'podcast hari ini indonesia' },
];
const PODCAST_TITLES = ['Podcast Terpopuler','Motivasi & Inspirasi','Trending Podcast','Misteri & Cerita','Podcast Viral','Podcast Hari Ini'];

let currentHomeFilter = 'all';

function filterHome(type, el) {
    // Update pill active state
    document.querySelectorAll('.home-pills .pill').forEach(p => p.classList.remove('active'));
    if (el) el.classList.add('active');
    currentHomeFilter = type;

    if (type === 'podcast') {
        // Ganti judul section
        const titleEls = document.querySelectorAll('.section-title');
        titleEls.forEach((t, i) => { if (PODCAST_TITLES[i-1]) t.innerText = PODCAST_TITLES[i-1]; });
        // Load podcast queries
        loadSectionRows(PODCAST_QUERIES);
        // Sembunyikan recent (sering didengarkan)
        const recentSec = document.querySelector('#recentList')?.closest('.section-container');
        if (recentSec) recentSec.style.display = 'none';
        const artistSec = document.querySelector('#rowArtists')?.closest('.section-container');
        if (artistSec) artistSec.style.display = 'none';
    } else if (type === 'music') {
        // Tampilkan semua section musik
        document.querySelectorAll('#view-home .section-container').forEach(s => s.style.display = '');
        applyLanguageTitles();
        loadSectionRows(getHomeQueries());
    } else {
        // Semua — tampilkan semua
        document.querySelectorAll('#view-home .section-container').forEach(s => s.style.display = '');
        applyLanguageTitles();
        loadHomeData();
    }
}

async function loadSectionRows(queries) {
    for (const row of queries) {
        const el = document.getElementById(row.id);
        if (!el) continue;
        el.innerHTML = '<div style="color:var(--text-sub);padding:8px 0;font-size:13px;">Memuat...</div>';
        try {
            const res = await apiFetch('/api/search?query=' + encodeURIComponent(row.query));
            const result = await res.json();
            if (result.status === 'success' && result.data.length > 0) {
                el.innerHTML = result.data.slice(0, 10).map(renderHCard).join('');
            } else {
                el.innerHTML = '<div style="color:var(--text-sub);padding:8px 0;font-size:13px;">Tidak ada hasil.</div>';
            }
        } catch(e) {
            el.innerHTML = '<div style="color:var(--text-sub);padding:8px 0;font-size:13px;">Gagal memuat.</div>';
        }
    }
}

"""

# Sisipkan setelah applyLanguageTitles
insert_after = "\n}\nconst HOME_QUERIES = ["
if insert_after in content:
    content = content.replace(insert_after, "\n}\n" + filter_home_fn + "const HOME_QUERIES = [", 1)
    print("OK: filterHome function added")
else:
    print("WARN: insert point not found")

with open('public/script.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
