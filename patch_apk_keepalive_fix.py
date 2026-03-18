with open('auspoty-apk/app/src/main/java/com/auspoty/app/MainActivity.java', 'r', encoding='utf-8') as f:
    java = f.read()

old_keepalive = '''                    webView.evaluateJavascript(
                        "(function(){" +
                        "  if(typeof ytPlayer!=='undefined'&&ytPlayer&&typeof ytPlayer.getPlayerState==='function'){" +
                        "    var s=ytPlayer.getPlayerState();" +
                        "    if(s===0){" + // ENDED
                        "      if(typeof isRepeat!=='undefined'&&isRepeat){ytPlayer.seekTo(0);ytPlayer.playVideo();}" +
                        "      else if(typeof playNextSimilarSong==='function'){playNextSimilarSong();}" +
                        "    } else if(s===2&&typeof isPlaying!=='undefined'&&isPlaying){" + // PAUSED tapi harusnya playing
                        "      ytPlayer.playVideo();" +
                        "    }" +
                        "  }" +
                        "  if(typeof _bgAudioCtx!=='undefined'&&_bgAudioCtx&&_bgAudioCtx.state==='suspended'){" +
                        "    _bgAudioCtx.resume();" +
                        "  }" +
                        "  return 1;" +
                        "})()", null);'''

new_keepalive = '''                    webView.evaluateJavascript(
                        "(function(){" +
                        "  if(typeof ytPlayer!=='undefined'&&ytPlayer&&typeof ytPlayer.getPlayerState==='function'){" +
                        "    var s=ytPlayer.getPlayerState();" +
                        // ENDED — gunakan flag _bgEndedHandling agar tidak double-trigger
                        "    if(s===0&&!window._bgEndedHandling){" +
                        "      window._bgEndedHandling=true;" +
                        "      if(typeof isRepeat!=='undefined'&&isRepeat){" +
                        "        ytPlayer.seekTo(0);ytPlayer.playVideo();" +
                        "        setTimeout(function(){window._bgEndedHandling=false;},3000);" +
                        "      } else if(typeof playNextSimilarSong==='function'){" +
                        "        playNextSimilarSong();" +
                        "        setTimeout(function(){window._bgEndedHandling=false;},5000);" +
                        "      }" +
                        "    } else if(s===1||s===3){" +
                        // Playing atau buffering — reset flag
                        "      window._bgEndedHandling=false;" +
                        "    } else if(s===2&&typeof isPlaying!=='undefined'&&isPlaying){" +
                        "      ytPlayer.playVideo();" +
                        "    }" +
                        "  }" +
                        "  if(typeof _bgAudioCtx!=='undefined'&&_bgAudioCtx&&_bgAudioCtx.state==='suspended'){" +
                        "    _bgAudioCtx.resume();" +
                        "  }" +
                        "  return 1;" +
                        "})()", null);'''

if old_keepalive in java:
    java = java.replace(old_keepalive, new_keepalive)
    print('OK: keepAliveRunnable fixed with _bgEndedHandling flag')
else:
    print('WARN: exact match not found, trying line-by-line...')
    # Cari dan ganti bagian ENDED saja
    old_ended_line = (
        '                        "    if(s===0){" + // ENDED\n'
        '                        "      if(typeof isRepeat!==\'undefined\'&&isRepeat){ytPlayer.seekTo(0);ytPlayer.playVideo();}" +\n'
        '                        "      else if(typeof playNextSimilarSong===\'function\'){playNextSimilarSong();}" +\n'
        '                        "    } else if(s===2&&typeof isPlaying!==\'undefined\'&&isPlaying){" + // PAUSED tapi harusnya playing\n'
        '                        "      ytPlayer.playVideo();" +\n'
        '                        "    }" +'
    )
    new_ended_line = (
        '                        "    if(s===0&&!window._bgEndedHandling){" +\n'
        '                        "      window._bgEndedHandling=true;" +\n'
        '                        "      if(typeof isRepeat!==\'undefined\'&&isRepeat){ytPlayer.seekTo(0);ytPlayer.playVideo();setTimeout(function(){window._bgEndedHandling=false;},3000);}" +\n'
        '                        "      else if(typeof playNextSimilarSong===\'function\'){playNextSimilarSong();setTimeout(function(){window._bgEndedHandling=false;},5000);}" +\n'
        '                        "    } else if(s===1||s===3){window._bgEndedHandling=false;}" +\n'
        '                        "    else if(s===2&&typeof isPlaying!==\'undefined\'&&isPlaying){ytPlayer.playVideo();}" +'
    )
    if old_ended_line in java:
        java = java.replace(old_ended_line, new_ended_line)
        print('OK: partial patch applied')
    else:
        # Coba ganti string sederhana
        java = java.replace(
            '"    if(s===0){" + // ENDED',
            '"    if(s===0\u0026\u0026!window._bgEndedHandling){" +'
        )
        java = java.replace(
            '"      if(typeof isRepeat!==\'undefined\'&&isRepeat){ytPlayer.seekTo(0);ytPlayer.playVideo();}"\n                        + "      else if(typeof playNextSimilarSong===\'function\'){playNextSimilarSong();}"',
            '"      if(typeof isRepeat!==\'undefined\'&&isRepeat){ytPlayer.seekTo(0);ytPlayer.playVideo();window._bgEndedHandling=false;}" +\n                        "      else if(typeof playNextSimilarSong===\'function\'){playNextSimilarSong();setTimeout(function(){window._bgEndedHandling=false;},5000);}"'
        )
        print('OK: minimal patch applied')

with open('auspoty-apk/app/src/main/java/com/auspoty/app/MainActivity.java', 'w', encoding='utf-8') as f:
    f.write(java)
print('MainActivity.java saved.')
print('DONE.')
