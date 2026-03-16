# Auspoty Android App

## Cara Build APK

### Syarat
- Android Studio (download di https://developer.android.com/studio)
- JDK 17+

### Langkah
1. Buka Android Studio
2. Pilih "Open" → pilih folder `auspoty-apk`
3. Tunggu Gradle sync selesai
4. Klik **Build → Build Bundle(s)/APK(s) → Build APK(s)**
5. APK ada di: `app/build/outputs/apk/debug/app-debug.apk`

### Untuk Play Store (Release APK)
1. Build → Generate Signed Bundle/APK
2. Pilih APK → buat keystore baru
3. Isi semua info → Build
4. Upload `app-release.apk` ke Play Console
