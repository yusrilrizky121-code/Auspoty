package com.auspoty.app

import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.webkit.WebView
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {

    private val CHANNEL = "com.auspoty.app/music"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "startMusicService" -> {
                    val title = call.argument<String>("title") ?: "Auspoty"
                    val artist = call.argument<String>("artist") ?: ""
                    startMusicService(title, artist)
                    result.success(null)
                }
                "stopMusicService" -> {
                    stopService(Intent(this, MusicForegroundService::class.java))
                    result.success(null)
                }
                "keepWebViewAlive" -> {
                    // Dipanggil dari Flutter saat app masuk background
                    // Tidak perlu lakukan apa-apa di sini — cukup acknowledge
                    result.success(null)
                }
                else -> result.notImplemented()
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WebView.setWebContentsDebuggingEnabled(false)
        // Start foreground service dari awal
        startMusicService("Auspoty", "Siap memutar musik")
    }

    override fun onPause() {
        super.onPause()
        // PENTING: Jangan panggil flutterView?.onPause() atau webView.onPause()
        // Flutter engine akan pause WebView secara default — kita cegah dengan
        // tidak memanggil apapun yang bisa pause WebView rendering/JS execution
    }

    override fun onResume() {
        super.onResume()
    }

    override fun onDestroy() {
        super.onDestroy()
        stopService(Intent(this, MusicForegroundService::class.java))
    }

    private fun startMusicService(title: String, artist: String) {
        val intent = Intent(this, MusicForegroundService::class.java).apply {
            putExtra("title", title)
            putExtra("artist", artist)
            action = "START"
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
    }
}
