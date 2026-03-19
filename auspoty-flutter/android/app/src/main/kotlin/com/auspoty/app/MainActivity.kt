package com.auspoty.app

import android.content.ComponentName
import android.content.Intent
import android.content.ServiceConnection
import android.os.Build
import android.os.Bundle
import android.os.IBinder
import android.webkit.WebView
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {

    companion object {
        const val CHANNEL = "com.auspoty.app/music"
    }

    private var musicService: MusicPlayerService? = null
    private var serviceBound = false
    private var methodChannel: MethodChannel? = null

    private val serviceConnection = object : ServiceConnection {
        override fun onServiceConnected(name: ComponentName?, binder: IBinder?) {
            musicService = (binder as MusicPlayerService.LocalBinder).getService()
            serviceBound = true
            MusicPlayerService.flutterChannel = methodChannel
        }
        override fun onServiceDisconnected(name: ComponentName?) {
            serviceBound = false
            musicService = null
        }
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        methodChannel = MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
        methodChannel!!.setMethodCallHandler { call, result ->
            when (call.method) {

                // Kirim Intent ke service — tidak butuh Flutter engine setelah ini
                "playByVideoId" -> {
                    val videoId = call.argument<String>("videoId") ?: ""
                    val title   = call.argument<String>("title")   ?: ""
                    val artist  = call.argument<String>("artist")  ?: ""
                    val thumb   = call.argument<String>("thumbnail") ?: ""
                    sendPlayIntent(videoId, title, artist, thumb)
                    result.success(null)
                }

                "playUrl" -> {
                    val url    = call.argument<String>("url")       ?: ""
                    val title  = call.argument<String>("title")     ?: ""
                    val artist = call.argument<String>("artist")    ?: ""
                    val thumb  = call.argument<String>("thumbnail") ?: ""
                    // Untuk playUrl langsung, bind ke service
                    ensureServiceStarted()
                    doWithService { it.playUrl(url, title, artist, thumb) }
                    result.success(null)
                }

                "pause"  -> {
                    sendActionIntent(MusicPlayerService.ACTION_PAUSE)
                    result.success(null)
                }
                "resume" -> {
                    sendActionIntent(MusicPlayerService.ACTION_RESUME)
                    result.success(null)
                }

                "seekTo" -> {
                    val ms = call.argument<Int>("positionMs") ?: 0
                    sendSeekIntent(ms.toLong())
                    result.success(null)
                }

                "isPlaying"   -> result.success(
                    musicService?.isPlaying() ?: MusicPlayerService.instance?.isPlaying() ?: false
                )
                "getPosition" -> result.success(
                    (musicService?.getPosition() ?: MusicPlayerService.instance?.getPosition() ?: 0L).toInt()
                )
                "getDuration" -> result.success(
                    (musicService?.getDuration() ?: MusicPlayerService.instance?.getDuration() ?: 0L).toInt()
                )

                "stopService" -> {
                    sendActionIntent(MusicPlayerService.ACTION_STOP)
                    result.success(null)
                }

                else -> result.notImplemented()
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WebView.setWebContentsDebuggingEnabled(false)
        ensureServiceStarted()
        bindMusicService()
    }

    override fun onResume() {
        super.onResume()
        MusicPlayerService.flutterChannel = methodChannel
        if (!serviceBound) bindMusicService()
    }

    override fun onDestroy() {
        if (serviceBound) {
            unbindService(serviceConnection)
            serviceBound = false
        }
        super.onDestroy()
    }

    /**
     * Kirim Intent ACTION_PLAY ke service.
     * Intent-based — tidak butuh Flutter engine, tidak butuh binding.
     * Ini yang membuat background audio bisa jalan.
     */
    private fun sendPlayIntent(videoId: String, title: String, artist: String, thumb: String) {
        val intent = Intent(this, MusicPlayerService::class.java).apply {
            action = MusicPlayerService.ACTION_PLAY
            putExtra(MusicPlayerService.EXTRA_VIDEO_ID,  videoId)
            putExtra(MusicPlayerService.EXTRA_TITLE,     title)
            putExtra(MusicPlayerService.EXTRA_ARTIST,    artist)
            putExtra(MusicPlayerService.EXTRA_THUMBNAIL, thumb)
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
    }

    private fun sendActionIntent(action: String) {
        val intent = Intent(this, MusicPlayerService::class.java).apply {
            this.action = action
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
    }

    private fun sendSeekIntent(ms: Long) {
        val intent = Intent(this, MusicPlayerService::class.java).apply {
            action = MusicPlayerService.ACTION_SEEK
            putExtra(MusicPlayerService.EXTRA_SEEK_MS, ms)
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
    }

    private fun doWithService(action: (MusicPlayerService) -> Unit) {
        val svc = musicService ?: MusicPlayerService.instance
        if (svc != null) {
            action(svc)
        } else {
            bindMusicService()
            android.os.Handler(mainLooper).postDelayed({
                (musicService ?: MusicPlayerService.instance)?.let { action(it) }
            }, 500)
        }
    }

    private fun ensureServiceStarted() {
        val intent = Intent(this, MusicPlayerService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
    }

    private fun bindMusicService() {
        if (!serviceBound) {
            bindService(
                Intent(this, MusicPlayerService::class.java),
                serviceConnection,
                BIND_AUTO_CREATE
            )
        }
    }
}
