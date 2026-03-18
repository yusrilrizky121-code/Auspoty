package com.auspoty.app

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.os.PowerManager
import androidx.core.app.NotificationCompat

class MusicForegroundService : Service() {

    private var wakeLock: PowerManager.WakeLock? = null
    private val CHANNEL_ID = "auspoty_music_channel"
    private val NOTIF_ID = 1

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()

        val pm = getSystemService(POWER_SERVICE) as PowerManager
        @Suppress("DEPRECATION")
        wakeLock = pm.newWakeLock(
            PowerManager.PARTIAL_WAKE_LOCK,
            "Auspoty::MusicWakeLock"
        )
        wakeLock?.setReferenceCounted(false)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val title = intent?.getStringExtra("title") ?: "Auspoty"
        val artist = intent?.getStringExtra("artist") ?: "Sedang diputar..."

        val notif = buildNotification(title, artist)
        startForeground(NOTIF_ID, notif)

        // Acquire WakeLock — jaga CPU tetap aktif
        if (wakeLock?.isHeld == false) {
            wakeLock?.acquire(6 * 60 * 60 * 1000L) // max 6 jam
        }

        // START_STICKY: Android akan restart service kalau di-kill
        return START_STICKY
    }

    override fun onTaskRemoved(rootIntent: Intent?) {
        // Saat user swipe app dari recent — restart service
        val restartIntent = Intent(applicationContext, MusicForegroundService::class.java)
        restartIntent.setPackage(packageName)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(restartIntent)
        } else {
            startService(restartIntent)
        }
        super.onTaskRemoved(rootIntent)
    }

    override fun onDestroy() {
        super.onDestroy()
        if (wakeLock?.isHeld == true) {
            try { wakeLock?.release() } catch (e: Exception) {}
        }
        stopForeground(STOP_FOREGROUND_REMOVE)
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun buildNotification(title: String, artist: String): Notification {
        val pendingIntent = PendingIntent.getActivity(
            this, 0,
            Intent(this, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_SINGLE_TOP or Intent.FLAG_ACTIVITY_CLEAR_TOP
            },
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(title)
            .setContentText(artist)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setSilent(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setCategory(NotificationCompat.CATEGORY_TRANSPORT)
            .setForegroundServiceBehavior(NotificationCompat.FOREGROUND_SERVICE_IMMEDIATE)
            .build()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Musik Sedang Diputar",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Notifikasi musik Auspoty"
                setSound(null, null)
                enableVibration(false)
                lockscreenVisibility = Notification.VISIBILITY_PUBLIC
            }
            val nm = getSystemService(NotificationManager::class.java)
            nm.createNotificationChannel(channel)
        }
    }
}
