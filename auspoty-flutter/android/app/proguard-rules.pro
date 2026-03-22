# Flutter core
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }
-dontwarn io.flutter.**

# InAppWebView
-keep class com.pichillilorenzo.flutter_inappwebview.** { *; }
-dontwarn com.pichillilorenzo.**

# Wakelock
-keep class xyz.luan.** { *; }

# App classes
-keep class com.auspoty.app.** { *; }

# WebView JS interface
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Kotlin minimal
-keep class kotlin.Metadata { *; }
-dontwarn kotlin.**

# AndroidX minimal
-keep class androidx.core.** { *; }
-keep class androidx.media.** { *; }
-dontwarn androidx.**

# Remove logging in release
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}

# Aggressive shrink
-optimizationpasses 5
-allowaccessmodification
-dontpreverify
