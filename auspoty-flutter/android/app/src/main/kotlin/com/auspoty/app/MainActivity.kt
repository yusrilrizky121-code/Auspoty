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
                    result.success(null)
                }
                else -> result.notImplemented()
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WebView.setWebContentsDebuggingEnabled(false)
        startMusicService("Auspoty", "Siap memutar musik")
    }

    override fun onPause() {
        // KRITIS: Jangan panggil super.onPause() yang akan pause Flutter engine
        // Flutter engine default akan pause WebView JS execution saat onPause
        // Kita bypass ini supaya audio tetap jalan di background
        // Hanya panggil Activity.onPause() langsung, skip FlutterActivity.onPause()
        try {
            val activityClass = android.app.Activity::class.java
            val onPauseMethod = activityClass.getDeclaredMethod("onPause")
            onPauseMethod.isAccessible = true
            onPauseMethod.invoke(this)
        } catch (e: Exception) {
            // Fallback: panggil super normal
            super.onPause()
        }
    }

    override fun onResume() {
        super.onResume()
    }

    override fun onStop() {
        // Jangan panggil super.onStop() — Flutter akan pause engine
        // Hanya panggil Activity.onStop()
        try {
            val activityClass = android.app.Activity::class.java
            val onStopMethod = activityClass.getDeclaredMethod("onStop")
            onStopMethod.isAccessible = true
            onStopMethod.invoke(this)
        } catch (e: Exception) {
            super.onStop()
        }
    }

    override fun onStart() {
        super.onStart()
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
