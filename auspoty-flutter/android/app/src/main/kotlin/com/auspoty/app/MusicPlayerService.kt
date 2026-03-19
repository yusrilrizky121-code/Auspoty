package com.auspoty.app

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Binder
import android.os.Build
import android.os.IBinder
import android.os.PowerManager
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.media3.common.AudioAttributes
import androidx.media3.common.C
import androidx.media3.common.MediaItem
import androidx.media3.common.MediaMetadata
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer
import io.flutter.plugin.common.MethodChannel
import kotlinx.coroutines.*
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

/**
 * MusicPlayerService — pure Service, self-contained.
 *
 * Cara kerja:
 * 1. Menerima Intent ACTION_PLAY dengan extras: videoId, title, artist, thumbnail
 * 2. Fetch stream URL sendiri via HTTP ke Vercel API (tidak butuh Flutter engine)
 * 3. ExoPlayer play audio — tetap jalan saat app di-background/swipe
 *
 * Tidak ada dependency ke Flutter MethodChannel untuk trigger play.
 * Flutter hanya dipakai untuk callback (onCompleted) saat app di-foreground.
 */
class MusicPlayerService : Service() {

    companion object {
        const val CHANNEL_ID   = "auspoty_player"
        const val NOTIF_ID     = 42
        const val API_BASE     = "https://clone2-git-master-yusrilrizky121-codes-projects.vercel.app"
        const val TAG          = "MusicPlayerService"

        // Intent actions
        const val ACTION_PLAY   = "com.auspoty.app.PLAY"
        const val ACTION_PAUSE  = "com.auspoty.app.PAUSE"
        const val ACTION_RESUME = "com.auspoty.app.RESUME"
        const val ACTION_STOP   = "com.auspoty.app.STOP"
        const val ACTION_SEEK   = "com.auspoty.app.SEEK"

        // Intent extras
        const val EXTRA_VIDEO_ID  = "videoId"
        const val EXTRA_TITLE     = "title"
        const val EXTRA_ARTIST    = "artist"
        const val EXTRA_THUMBNAIL = "thumbnail"
        const val EXTRA_SEEK_MS   = "seekMs"

        // Singleton untuk akses dari MainActivity
        var flutterChannel: MethodChannel? = null
        var instance: MusicPlayerService? = null
    }

    private lateinit var player: ExoPlayer
    private var wakeLock: PowerManager.WakeLock? = null
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    private var currentTitle  = "Auspoty"
    private var currentArtist = ""

    // Binder untuk MainActivity bind ke service
    inner class LocalBinder : Binder() {
        fun getService() = this@MusicPlayerService
    }
    private val binder = LocalBinder()

    override fun onBind(intent: Intent?): IBinder = binder

    override fun onCreate() {
        super.onCreate()
        instance = this
        createNotificationChannel()

        // WakeLock — CPU tetap aktif saat layar mati
        val pm = getSystemService(POWER_SERVICE) as PowerManager
        @Suppress("DEPRECATION")
        wakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "Auspoty::PlayerWakeLock")
        wakeLock?.setReferenceCounted(false)

        // ExoPlayer setup
        player = ExoPlayer.Builder(this).build().apply {
            setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(C.USAGE_MEDIA)
                    .setContentType(C.CONTENT_TYPE_MUSIC)
                    .build(),
                true
            )
            addListener(object : Player.Listener {
                override fun onPlaybackStateChanged(state: Int) {
                    if (state == Player.STATE_ENDED) {
                        scope.launch {
                            // Callback ke Flutter jika engine aktif
                            flutterChannel?.invokeMethod("onCompleted", null)
                        }
                    }
                }
            })
        }

        // Langsung start foreground
        startForegroundCompat(buildNotification("Auspoty", "Siap memutar musik"))
        Log.d(TAG, "Service created")
    }

    /**
     * Semua perintah masuk via Intent — tidak butuh Flutter engine sama sekali.
     * Ini yang membuat background audio bisa jalan.
     */
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_PLAY -> {
                val videoId  = intent.getStringExtra(EXTRA_VIDEO_ID)  ?: return START_STICKY
                val title    = intent.getStringExtra(EXTRA_TITLE)     ?: ""
                val artist   = intent.getStringExtra(EXTRA_ARTIST)    ?: ""
                val thumbUrl = intent.getStringExtra(EXTRA_THUMBNAIL) ?: ""
                playByVideoId(videoId, title, artist, thumbUrl)
            }
            ACTION_PAUSE  -> pausePlayer()
            ACTION_RESUME -> resumePlayer()
            ACTION_STOP   -> { stopPlayer(); stopSelf() }
            ACTION_SEEK   -> {
                val ms = intent.getLongExtra(EXTRA_SEEK_MS, -1L)
                if (ms >= 0) player.seekTo(ms)
            }
        }
        return START_STICKY
    }

    /**
     * Fetch stream URL dari Vercel API, lalu play.
     * Semua di background thread — tidak butuh Flutter engine.
     */
    private fun playByVideoId(videoId: String, title: String, artist: String, thumbUrl: String) {
        currentTitle  = title.ifEmpty { "Auspoty" }
        currentArtist = artist
        startForegroundCompat(buildNotification(currentTitle, "Memuat..."))

        scope.launch(Dispatchers.IO) {
            try {
                Log.d(TAG, "Fetching stream URL for: $videoId")
                val streamUrl = fetchStreamUrl(videoId)
                if (streamUrl != null) {
                    Log.d(TAG, "Got URL, playing")
                    withContext(Dispatchers.Main) {
                        playUrl(streamUrl, title, artist, thumbUrl)
                    }
                } else {
                    Log.e(TAG, "fetchStreamUrl returned null")
                    withContext(Dispatchers.Main) {
                        startForegroundCompat(buildNotification(currentTitle, "Gagal memuat"))
                    }
                }
            } catch (e: Exception) {
                Log.e(TAG, "playByVideoId error: ${e.message}")
            }
        }
    }

    private fun fetchStreamUrl(videoId: String): String? {
        return try {
            val url  = URL("$API_BASE/api/stream")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "POST"
            conn.setRequestProperty("Content-Type", "application/json")
            conn.setRequestProperty("Accept", "application/json")
            conn.doOutput      = true
            conn.connectTimeout = 30_000
            conn.readTimeout    = 60_000

            val body = """{"videoId":"$videoId"}"""
            conn.outputStream.use { it.write(body.toByteArray(Charsets.UTF_8)) }

            val code = conn.responseCode
            Log.d(TAG, "API response: $code")
            if (code == 200) {
                val text = conn.inputStream.bufferedReader(Charsets.UTF_8).readText()
                val json = JSONObject(text)
                if (json.optString("status") == "success") {
                    json.optString("url").takeIf { it.isNotEmpty() }
                } else {
                    Log.e(TAG, "API error: ${json.optString("message")}")
                    null
                }
            } else null
        } catch (e: Exception) {
            Log.e(TAG, "fetchStreamUrl: ${e.message}")
            null
        }
    }

    fun playUrl(url: String, title: String, artist: String, thumbUrl: String) {
        currentTitle  = title.ifEmpty { "Auspoty" }
        currentArtist = artist

        val item = MediaItem.Builder()
            .setUri(url)
            .setMediaMetadata(
                MediaMetadata.Builder()
                    .setTitle(currentTitle)
                    .setArtist(currentArtist)
                    .setArtworkUri(
                        if (thumbUrl.isNotEmpty()) android.net.Uri.parse(thumbUrl) else null
                    )
                    .build()
            )
            .build()

        player.setMediaItem(item)
        player.prepare()
        player.play()

        if (wakeLock?.isHeld == false) wakeLock?.acquire(6 * 60 * 60 * 1000L)
        startForegroundCompat(buildNotification(currentTitle, currentArtist))
        Log.d(TAG, "Playing: $currentTitle")
    }

    fun pausePlayer()  { player.pause() }
    fun resumePlayer() { player.play() }
    fun stopPlayer()   { player.stop(); player.clearMediaItems() }
    fun seekTo(ms: Long) { player.seekTo(ms) }
    fun isPlaying()      = player.isPlaying
    fun getPosition()    = player.currentPosition
    fun getDuration()    = if (player.duration == C.TIME_UNSET) 0L else player.duration

    /**
     * Saat app di-swipe dari recents:
     * - Musik playing → biarkan jalan
     * - Tidak playing → stop service
     */
    override fun onTaskRemoved(rootIntent: Intent?) {
        Log.d(TAG, "onTaskRemoved, isPlaying=${player.isPlaying}")
        if (!player.isPlaying) stopSelf()
        // Tidak call super — cegah Android auto-stop
    }

    override fun onDestroy() {
        Log.d(TAG, "Service destroyed")
        scope.cancel()
        player.release()
        if (wakeLock?.isHeld == true) try { wakeLock?.release() } catch (_: Exception) {}
        instance = null
        super.onDestroy()
    }

    private fun startForegroundCompat(notification: Notification) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            startForeground(NOTIF_ID, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK)
        } else {
            startForeground(NOTIF_ID, notification)
        }
    }

    private fun buildNotification(title: String, text: String): Notification {
        val pi = PendingIntent.getActivity(
            this, 0,
            Intent(this, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_SINGLE_TOP or Intent.FLAG_ACTIVITY_CLEAR_TOP
            },
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(title)
            .setContentText(text.ifEmpty { "Sedang memutar" })
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentIntent(pi)
            .setOngoing(true)
            .setSilent(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setCategory(NotificationCompat.CATEGORY_TRANSPORT)
            .build()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val ch = NotificationChannel(
                CHANNEL_ID, "Auspoty Music", NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Kontrol musik Auspoty"
                setSound(null, null)
                enableVibration(false)
                lockscreenVisibility = Notification.VISIBILITY_PUBLIC
            }
            (getSystemService(NOTIFICATION_SERVICE) as NotificationManager)
                .createNotificationChannel(ch)
        }
    }
}
