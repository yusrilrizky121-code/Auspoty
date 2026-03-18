package com.auspoty.app

import android.app.*
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.*
import android.support.v4.media.MediaMetadataCompat
import android.support.v4.media.session.MediaSessionCompat
import android.support.v4.media.session.PlaybackStateCompat
import androidx.core.app.NotificationCompat
import androidx.media.app.NotificationCompat.MediaStyle
import com.google.android.exoplayer2.*
import com.google.android.exoplayer2.audio.AudioAttributes
import kotlinx.coroutines.*
import java.net.URL

class MusicPlayerService : Service() {

    companion object {
        const val CHANNEL_ID = "auspoty_player"
        const val NOTIF_ID = 42
        const val ACTION_PLAY = "ACTION_PLAY"
        const val ACTION_PAUSE = "ACTION_PAUSE"
        const val ACTION_NEXT = "ACTION_NEXT"
        const val ACTION_PREV = "ACTION_PREV"
        const val ACTION_STOP = "ACTION_STOP"

        var flutterChannel: io.flutter.plugin.common.MethodChannel? = null
        var instance: MusicPlayerService? = null
    }

    private lateinit var player: SimpleExoPlayer
    private lateinit var mediaSession: MediaSessionCompat
    private var wakeLock: PowerManager.WakeLock? = null
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    private var currentTitle = "Auspoty"
    private var currentArtist = ""
    private var currentThumb = ""
    private var artBitmap: Bitmap? = null

    inner class LocalBinder : Binder() {
        fun getService() = this@MusicPlayerService
    }
    private val binder = LocalBinder()

    override fun onBind(intent: Intent?) = binder

    override fun onCreate() {
        super.onCreate()
        instance = this
        createNotificationChannel()

        // WakeLock agar CPU tidak sleep saat audio jalan
        val pm = getSystemService(POWER_SERVICE) as PowerManager
        @Suppress("DEPRECATION")
        wakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "Auspoty::PlayerWakeLock")
        wakeLock?.setReferenceCounted(false)

        // MediaSession untuk kontrol dari notifikasi / headset / lock screen
        mediaSession = MediaSessionCompat(this, "AuspotyPlayer").apply {
            setCallback(object : MediaSessionCompat.Callback() {
                override fun onPlay() { player.play() ; updateNotification() }
                override fun onPause() { player.pause() ; updateNotification() }
                override fun onSkipToNext() {
                    scope.launch(Dispatchers.Main) { flutterChannel?.invokeMethod("onNext", null) }
                }
                override fun onSkipToPrevious() {
                    scope.launch(Dispatchers.Main) { flutterChannel?.invokeMethod("onPrev", null) }
                }
                override fun onStop() { stopSelf() }
                override fun onSeekTo(pos: Long) { player.seekTo(pos) }
            })
            isActive = true
        }

        // ExoPlayer dengan audio attributes yang benar
        val audioAttr = AudioAttributes.Builder()
            .setUsage(C.USAGE_MEDIA)
            .setContentType(C.CONTENT_TYPE_MUSIC)
            .build()

        player = SimpleExoPlayer.Builder(this).build().apply {
            setAudioAttributes(audioAttr, /* handleAudioFocus= */ true)
            addListener(object : Player.Listener {
                override fun onPlaybackStateChanged(state: Int) {
                    updatePlaybackState()
                    updateNotification()
                    if (state == Player.STATE_ENDED) {
                        scope.launch(Dispatchers.Main) {
                            flutterChannel?.invokeMethod("onCompleted", null)
                        }
                    }
                }
                override fun onIsPlayingChanged(isPlaying: Boolean) {
                    updatePlaybackState()
                    updateNotification()
                }
            })
        }

        // Start foreground dengan notifikasi kosong dulu
        startForeground(NOTIF_ID, buildNotification())
    }

    fun playUrl(url: String, title: String, artist: String, thumbUrl: String) {
        currentTitle = title
        currentArtist = artist
        currentThumb = thumbUrl

        // Load artwork di background
        scope.launch(Dispatchers.IO) {
            artBitmap = try {
                val bmp = BitmapFactory.decodeStream(URL(thumbUrl).openStream())
                bmp
            } catch (e: Exception) { null }
            withContext(Dispatchers.Main) { updateNotification() }
        }

        val mediaItem = MediaItem.fromUri(url)
        player.setMediaItem(mediaItem)
        player.prepare()
        player.play()

        if (wakeLock?.isHeld == false) wakeLock?.acquire(6 * 60 * 60 * 1000L)

        updateMediaSessionMetadata()
        updateNotification()
    }

    fun pause() {
        player.pause()
        updateNotification()
    }

    fun resume() {
        player.play()
        updateNotification()
    }

    fun seekTo(posMs: Long) {
        player.seekTo(posMs)
    }

    fun isPlaying() = player.isPlaying
    fun currentPosition() = player.currentPosition
    fun duration() = player.duration.takeIf { it != C.TIME_UNSET } ?: 0L

    private fun updateMediaSessionMetadata() {
        val meta = MediaMetadataCompat.Builder()
            .putString(MediaMetadataCompat.METADATA_KEY_TITLE, currentTitle)
            .putString(MediaMetadataCompat.METADATA_KEY_ARTIST, currentArtist)
            .putLong(MediaMetadataCompat.METADATA_KEY_DURATION, duration())
            .apply { artBitmap?.let { putBitmap(MediaMetadataCompat.METADATA_KEY_ART, it) } }
            .build()
        mediaSession.setMetadata(meta)
    }

    private fun updatePlaybackState() {
        val state = if (player.isPlaying) PlaybackStateCompat.STATE_PLAYING
                    else PlaybackStateCompat.STATE_PAUSED
        val pb = PlaybackStateCompat.Builder()
            .setState(state, player.currentPosition, 1f)
            .setActions(
                PlaybackStateCompat.ACTION_PLAY or
                PlaybackStateCompat.ACTION_PAUSE or
                PlaybackStateCompat.ACTION_SKIP_TO_NEXT or
                PlaybackStateCompat.ACTION_SKIP_TO_PREVIOUS or
                PlaybackStateCompat.ACTION_SEEK_TO
            )
            .build()
        mediaSession.setPlaybackState(pb)
    }

    private fun updateNotification() {
        val nm = getSystemService(NOTIFICATION_SERVICE) as NotificationManager
        nm.notify(NOTIF_ID, buildNotification())
    }

    private fun buildNotification(): Notification {
        val pi = PendingIntent.getActivity(
            this, 0,
            Intent(this, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_SINGLE_TOP or Intent.FLAG_ACTIVITY_CLEAR_TOP
            },
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        fun actionPi(action: String, reqCode: Int): PendingIntent {
            val i = Intent(this, MusicPlayerService::class.java).apply { this.action = action }
            return PendingIntent.getService(this, reqCode, i,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
        }

        val isPlaying = player.isPlaying
        val playPauseIcon = if (isPlaying) android.R.drawable.ic_media_pause
                           else android.R.drawable.ic_media_play
        val playPauseAction = if (isPlaying) ACTION_PAUSE else ACTION_PLAY

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(currentTitle)
            .setContentText(currentArtist)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setLargeIcon(artBitmap)
            .setContentIntent(pi)
            .setOngoing(isPlaying)
            .setSilent(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setCategory(NotificationCompat.CATEGORY_TRANSPORT)
            .addAction(android.R.drawable.ic_media_previous, "Prev", actionPi(ACTION_PREV, 1))
            .addAction(playPauseIcon, if (isPlaying) "Pause" else "Play", actionPi(playPauseAction, 2))
            .addAction(android.R.drawable.ic_media_next, "Next", actionPi(ACTION_NEXT, 3))
            .setStyle(
                MediaStyle()
                    .setMediaSession(mediaSession.sessionToken)
                    .setShowActionsInCompactView(0, 1, 2)
            )
            .build()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_PLAY   -> { player.play(); updateNotification() }
            ACTION_PAUSE  -> { player.pause(); updateNotification() }
            ACTION_NEXT   -> scope.launch(Dispatchers.Main) { flutterChannel?.invokeMethod("onNext", null) }
            ACTION_PREV   -> scope.launch(Dispatchers.Main) { flutterChannel?.invokeMethod("onPrev", null) }
            ACTION_STOP   -> stopSelf()
        }
        return START_STICKY
    }

    override fun onTaskRemoved(rootIntent: Intent?) {
        // Tetap jalan saat app di-swipe dari recent
        super.onTaskRemoved(rootIntent)
    }

    override fun onDestroy() {
        scope.cancel()
        player.release()
        mediaSession.release()
        if (wakeLock?.isHeld == true) try { wakeLock?.release() } catch (_: Exception) {}
        instance = null
        super.onDestroy()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val ch = NotificationChannel(CHANNEL_ID, "Auspoty Music", NotificationManager.IMPORTANCE_LOW).apply {
                description = "Kontrol musik Auspoty"
                setSound(null, null)
                enableVibration(false)
                lockscreenVisibility = Notification.VISIBILITY_PUBLIC
            }
            (getSystemService(NOTIFICATION_SERVICE) as NotificationManager).createNotificationChannel(ch)
        }
    }
}
