JS_PATH = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# ============================================================
# FIX 1: Tambah fungsi applyUILanguage() setelah applyLanguageTitles()
# ============================================================
UI_LANG_FUNC = """
// UI LANGUAGE TRANSLATIONS
const UI_STRINGS = {
    Indonesia: {
        navHome: 'Home', navSearch: 'Cari', navLibrary: 'Koleksi', navSettings: 'Pengaturan',
        searchPlaceholder: 'Apa yang ingin kamu dengarkan?',
        searchTitle: 'Cari',
        searchBrowse: 'Jelajahi semua',
        libTitle: 'Koleksi Kamu',
        settingsTitle: 'Pengaturan',
        settingsDisplay: 'Tampilan',
        settingsLangRegion: 'Bahasa & Wilayah',
        settingsPlayback: 'Pemutaran',
        settingsNotif: 'Notifikasi',
        settingsStorage: 'Penyimpanan & Data',
        settingsAbout: 'Tentang',
        settingsTheme: 'Tema Warna',
        settingsDark: 'Mode Gelap',
        settingsQuality: 'Kualitas Audio',
        settingsFontSize: 'Ukuran Teks',
        settingsLang: 'Bahasa Aplikasi',
        settingsRegion: 'Wilayah Konten',
        settingsAutoplay: 'Putar Otomatis',
        settingsCrossfade: 'Crossfade',
        settingsNormalize: 'Normalisasi Volume',
        settingsLyricsSync: 'Sinkronisasi Lirik',
        settingsNotifSong: 'Notifikasi Lagu',
        settingsNotifRelease: 'Rilis Baru',
        settingsClearCache: 'Hapus Cache',
        settingsClearLiked: 'Hapus Lagu Disukai',
        settingsDeveloper: 'Developer',
        settingsVersion: 'Versi Aplikasi',
        loginGoogle: 'Masuk dengan Google',
        loginSub: 'Sinkronkan data kamu',
        logoutGoogle: 'Keluar dari Google',
        homePillAll: 'Semua', homePillMusic: 'Musik', homePillPodcast: 'Podcast',
    },
    English: {
        navHome: 'Home', navSearch: 'Search', navLibrary: 'Library', navSettings: 'Settings',
        searchPlaceholder: 'What do you want to listen to?',
        searchTitle: 'Search',
        searchBrowse: 'Browse all',
        libTitle: 'Your Library',
        settingsTitle: 'Settings',
        settingsDisplay: 'Display',
        settingsLangRegion: 'Language & Region',
        settingsPlayback: 'Playback',
        settingsNotif: 'Notifications',
        settingsStorage: 'Storage & Data',
        settingsAbout: 'About',
        settingsTheme: 'Color Theme',
        settingsDark: 'Dark Mode',
        settingsQuality: 'Audio Quality',
        settingsFontSize: 'Text Size',
        settingsLang: 'App Language',
        settingsRegion: 'Content Region',
        settingsAutoplay: 'Autoplay',
        settingsCrossfade: 'Crossfade',
        settingsNormalize: 'Volume Normalization',
        settingsLyricsSync: 'Lyrics Sync',
        settingsNotifSong: 'Now Playing Notification',
        settingsNotifRelease: 'New Releases',
        settingsClearCache: 'Clear Cache',
        settingsClearLiked: 'Clear Liked Songs',
        settingsDeveloper: 'Developer',
        settingsVersion: 'App Version',
        loginGoogle: 'Sign in with Google',
        loginSub: 'Sync your data',
        logoutGoogle: 'Sign out from Google',
        homePillAll: 'All', homePillMusic: 'Music', homePillPodcast: 'Podcast',
    },
    Japanese: {
        navHome: 'ホーム', navSearch: '検索', navLibrary: 'ライブラリ', navSettings: '設定',
        searchPlaceholder: '何を聴きたいですか？',
        searchTitle: '検索',
        searchBrowse: 'すべて見る',
        libTitle: 'あなたのライブラリ',
        settingsTitle: '設定',
        settingsDisplay: '表示',
        settingsLangRegion: '言語と地域',
        settingsPlayback: '再生',
        settingsNotif: '通知',
        settingsStorage: 'ストレージとデータ',
        settingsAbout: 'アプリについて',
        settingsTheme: 'カラーテーマ',
        settingsDark: 'ダークモード',
        settingsQuality: '音質',
        settingsFontSize: '文字サイズ',
        settingsLang: 'アプリの言語',
        settingsRegion: 'コンテンツ地域',
        settingsAutoplay: '自動再生',
        settingsCrossfade: 'クロスフェード',
        settingsNormalize: '音量正規化',
        settingsLyricsSync: '歌詞同期',
        settingsNotifSong: '再生中の通知',
        settingsNotifRelease: '新着リリース',
        settingsClearCache: 'キャッシュを削除',
        settingsClearLiked: 'お気に入りを削除',
        settingsDeveloper: '開発者',
        settingsVersion: 'アプリバージョン',
        loginGoogle: 'Googleでサインイン',
        loginSub: 'データを同期する',
        logoutGoogle: 'Googleからサインアウト',
        homePillAll: 'すべて', homePillMusic: '音楽', homePillPodcast: 'ポッドキャスト',
    },
    Korean: {
        navHome: '홈', navSearch: '검색', navLibrary: '보관함', navSettings: '설정',
        searchPlaceholder: '무엇을 듣고 싶으세요?',
        searchTitle: '검색',
        searchBrowse: '모두 보기',
        libTitle: '내 보관함',
        settingsTitle: '설정',
        settingsDisplay: '디스플레이',
        settingsLangRegion: '언어 및 지역',
        settingsPlayback: '재생',
        settingsNotif: '알림',
        settingsStorage: '저장소 및 데이터',
        settingsAbout: '앱 정보',
        settingsTheme: '색상 테마',
        settingsDark: '다크 모드',
        settingsQuality: '음질',
        settingsFontSize: '텍스트 크기',
        settingsLang: '앱 언어',
        settingsRegion: '콘텐츠 지역',
        settingsAutoplay: '자동 재생',
        settingsCrossfade: '크로스페이드',
        settingsNormalize: '볼륨 정규화',
        settingsLyricsSync: '가사 동기화',
        settingsNotifSong: '재생 중 알림',
        settingsNotifRelease: '새 릴리스',
        settingsClearCache: '캐시 지우기',
        settingsClearLiked: '좋아요 삭제',
        settingsDeveloper: '개발자',
        settingsVersion: '앱 버전',
        loginGoogle: 'Google로 로그인',
        loginSub: '데이터 동기화',
        logoutGoogle: 'Google에서 로그아웃',
        homePillAll: '전체', homePillMusic: '음악', homePillPodcast: '팟캐스트',
    },
};

function applyUILanguage() {
    const lang = getSettings().language || 'Indonesia';
    const t = UI_STRINGS[lang] || UI_STRINGS.Indonesia;
    function setText(id, val) { const el = document.getElementById(id); if (el) el.innerText = val; }
    function setAttr(id, attr, val) { const el = document.getElementById(id); if (el) el.setAttribute(attr, val); }
    function setQueryAll(sel, val) { document.querySelectorAll(sel).forEach(el => { if (el.innerText.trim()) el.innerText = val; }); }

    // Nav items
    const navItems = document.querySelectorAll('.nav-item');
    if (navItems[0]) navItems[0].childNodes[navItems[0].childNodes.length-1].textContent = t.navHome;
    if (navItems[1]) navItems[1].childNodes[navItems[1].childNodes.length-1].textContent = t.navSearch;
    if (navItems[2]) navItems[2].childNodes[navItems[2].childNodes.length-1].textContent = t.navLibrary;
    if (navItems[3]) navItems[3].childNodes[navItems[3].childNodes.length-1].textContent = t.navSettings;

    // Search
    setAttr('searchInput', 'placeholder', t.searchPlaceholder);
    const searchH1 = document.querySelector('#view-search .search-header-container h1');
    if (searchH1) searchH1.innerText = t.searchTitle;
    const browseTitle = document.querySelector('#searchCategoriesUI .section-title');
    if (browseTitle) browseTitle.innerText = t.searchBrowse;

    // Library
    const libTitle = document.querySelector('.lib-title');
    if (libTitle) libTitle.innerText = t.libTitle;

    // Settings header
    const settH1 = document.querySelector('#view-settings .settings-header h1');
    if (settH1) settH1.innerText = t.settingsTitle;

    // Settings group labels
    const groupLabels = document.querySelectorAll('.settings-group-label');
    const labelKeys = ['settingsDisplay','settingsLangRegion','settingsPlayback','settingsNotif','settingsStorage','settingsAbout'];
    groupLabels.forEach((el, i) => { if (labelKeys[i] && t[labelKeys[i]]) el.innerText = t[labelKeys[i]]; });

    // Settings item titles (by order in settings groups)
    const allSettingsTitles = document.querySelectorAll('.settings-item-title');
    const titleMap = [
        null, // login/logout - skip
        null,
        t.settingsTheme,
        t.settingsDark,
        t.settingsQuality,
        t.settingsFontSize,
        t.settingsLang,
        t.settingsRegion,
        t.settingsAutoplay,
        t.settingsCrossfade,
        t.settingsNormalize,
        t.settingsLyricsSync,
        t.settingsNotifSong,
        t.settingsNotifRelease,
        t.settingsClearCache,
        t.settingsClearLiked,
        t.settingsDeveloper,
        t.settingsVersion,
    ];
    // Lebih aman: cari by ID atau data attribute
    // Gunakan querySelector dengan text matching
    const settingsItemMap = {
        'Tema Warna': t.settingsTheme, 'Color Theme': t.settingsTheme, 'カラーテーマ': t.settingsTheme, '색상 테마': t.settingsTheme,
        'Mode Gelap': t.settingsDark, 'Dark Mode': t.settingsDark, 'ダークモード': t.settingsDark, '다크 모드': t.settingsDark,
        'Kualitas Audio': t.settingsQuality, 'Audio Quality': t.settingsQuality, '音質': t.settingsQuality, '음질': t.settingsQuality,
        'Ukuran Teks': t.settingsFontSize, 'Text Size': t.settingsFontSize, '文字サイズ': t.settingsFontSize, '텍스트 크기': t.settingsFontSize,
        'Bahasa Aplikasi': t.settingsLang, 'App Language': t.settingsLang, 'アプリの言語': t.settingsLang, '앱 언어': t.settingsLang,
        'Wilayah Konten': t.settingsRegion, 'Content Region': t.settingsRegion, 'コンテンツ地域': t.settingsRegion, '콘텐츠 지역': t.settingsRegion,
        'Putar Otomatis': t.settingsAutoplay, 'Autoplay': t.settingsAutoplay, '自動再生': t.settingsAutoplay, '자동 재생': t.settingsAutoplay,
        'Crossfade': t.settingsCrossfade, 'クロスフェード': t.settingsCrossfade, '크로스페이드': t.settingsCrossfade,
        'Normalisasi Volume': t.settingsNormalize, 'Volume Normalization': t.settingsNormalize, '音量正規化': t.settingsNormalize, '볼륨 정규화': t.settingsNormalize,
        'Sinkronisasi Lirik': t.settingsLyricsSync, 'Lyrics Sync': t.settingsLyricsSync, '歌詞同期': t.settingsLyricsSync, '가사 동기화': t.settingsLyricsSync,
        'Notifikasi Lagu': t.settingsNotifSong, 'Now Playing Notification': t.settingsNotifSong, '再生中の通知': t.settingsNotifSong, '재생 중 알림': t.settingsNotifSong,
        'Rilis Baru': t.settingsNotifRelease, 'New Releases': t.settingsNotifRelease, '新着リリース': t.settingsNotifRelease, '새 릴리스': t.settingsNotifRelease,
        'Hapus Cache': t.settingsClearCache, 'Clear Cache': t.settingsClearCache, 'キャッシュを削除': t.settingsClearCache, '캐시 지우기': t.settingsClearCache,
        'Hapus Lagu Disukai': t.settingsClearLiked, 'Clear Liked Songs': t.settingsClearLiked, 'お気に入りを削除': t.settingsClearLiked, '좋아요 삭제': t.settingsClearLiked,
        'Developer': t.settingsDeveloper,
        'Versi Aplikasi': t.settingsVersion, 'App Version': t.settingsVersion, 'アプリバージョン': t.settingsVersion, '앱 버전': t.settingsVersion,
        'Masuk dengan Google': t.loginGoogle, 'Sign in with Google': t.loginGoogle, 'Googleでサインイン': t.loginGoogle, 'Google로 로그인': t.loginGoogle,
    };
    document.querySelectorAll('.settings-item-title').forEach(el => {
        const txt = el.innerText.trim();
        if (settingsItemMap[txt]) el.innerText = settingsItemMap[txt];
    });

    // Login/logout sub text
    setText('googleLoginText', t.loginGoogle);
    setText('googleLoginSub', t.loginSub);

    // Home pills
    const pills = document.querySelectorAll('#view-home .pill');
    if (pills[0]) pills[0].innerText = t.homePillAll;
    if (pills[1]) pills[1].innerText = t.homePillMusic;
    if (pills[2]) pills[2].innerText = t.homePillPodcast;
}
"""

# Insert setelah applyLanguageTitles function
insert_after = "function applyLanguageTitles() {"
idx = js.find(insert_after)
if idx != -1:
    # Find end of applyLanguageTitles
    end_idx = js.find('\n}', idx) + 2
    js = js[:end_idx] + '\n' + UI_LANG_FUNC + js[end_idx:]
    print('UI_LANG_FUNC inserted after applyLanguageTitles')
else:
    print('ERROR: applyLanguageTitles not found')

# ============================================================
# FIX 2: Panggil applyUILanguage() dari applyAllSettings()
# ============================================================
old_apply = "    estimateCacheSize();\n}"
new_apply = "    estimateCacheSize();\n    applyUILanguage();\n}"

if old_apply in js:
    js = js.replace(old_apply, new_apply, 1)
    print('applyUILanguage() call added to applyAllSettings')
else:
    print('WARNING: estimateCacheSize pattern not found')

# ============================================================
# FIX 3: Panggil applyUILanguage() dari loadHomeData() juga
# ============================================================
old_load = "    applyLanguageTitles();\n    for (const row of getHomeQueries())"
new_load = "    applyLanguageTitles();\n    applyUILanguage();\n    for (const row of getHomeQueries())"

if old_load in js:
    js = js.replace(old_load, new_load, 1)
    print('applyUILanguage() call added to loadHomeData')
else:
    print('WARNING: applyLanguageTitles pattern in loadHomeData not found')

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

print('\nDone. File saved.')
