package com.auspoty.app;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import androidx.appcompat.app.AppCompatActivity;

/**
 * Login Activity — cara persis seperti Metrolist:
 * Buka WebView ke Google login → redirect ke music.youtube.com → ambil cookie
 * Tidak perlu Google Cloud Console / OAuth setup apapun.
 */
public class LoginActivity extends AppCompatActivity {

    private WebView webView;
    private ProgressBar progressBar;
    private String visitorData = "";
    private String dataSyncId = "";
    private boolean hasCompletedLogin = false;

    private static final String LOGIN_URL =
        "https://accounts.google.com/ServiceLogin?continue=" +
        "https%3A%2F%2Fmusic.youtube.com";

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        webView = findViewById(R.id.loginWebView);
        progressBar = findViewById(R.id.loginProgress);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setSupportZoom(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);
        // User agent normal supaya Google tidak blokir
        settings.setUserAgentString(
            "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 " +
            "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        );

        // JavaScript interface — ambil VISITOR_DATA dan DATASYNC_ID seperti Metrolist
        webView.addJavascriptInterface(new Object() {
            @JavascriptInterface
            public void onRetrieveVisitorData(String data) {
                if (data != null && !data.isEmpty()) visitorData = data;
            }
            @JavascriptInterface
            public void onRetrieveDataSyncId(String data) {
                if (data != null && !data.isEmpty()) {
                    dataSyncId = data.contains("||") ? data.split("\\|\\|")[0] : data;
                }
            }
        }, "Android");

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                if (newProgress < 100) {
                    progressBar.setVisibility(View.VISIBLE);
                    progressBar.setProgress(newProgress);
                } else {
                    progressBar.setVisibility(View.GONE);
                }
            }
        });

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                // Ambil VISITOR_DATA dan DATASYNC_ID dari YouTube config
                view.loadUrl("javascript:Android.onRetrieveVisitorData(window.yt && window.yt.config_ ? window.yt.config_.VISITOR_DATA : '')");
                view.loadUrl("javascript:Android.onRetrieveDataSyncId(window.yt && window.yt.config_ ? window.yt.config_.DATASYNC_ID : '')");

                // Cek apakah sudah redirect ke music.youtube.com (login berhasil)
                if (url != null && url.startsWith("https://music.youtube.com") && !hasCompletedLogin) {
                    hasCompletedLogin = true;
                    String cookie = CookieManager.getInstance().getCookie(url);
                    if (cookie != null && !cookie.isEmpty()) {
                        saveLoginData(cookie, view);
                    }
                }
            }
        });

        // Hapus cookie lama supaya tidak auto-login dengan akun sebelumnya
        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(webView, true);

        webView.loadUrl(LOGIN_URL);
    }

    private void saveLoginData(String cookie, WebView view) {
        // Ambil nama & email dari halaman YouTube Music
        view.evaluateJavascript(
            "(function() {" +
            "  try {" +
            "    var name = document.querySelector('yt-formatted-string.ytmusic-nav-bar') || " +
            "               document.querySelector('[class*=\"account-name\"]');" +
            "    return name ? name.innerText : '';" +
            "  } catch(e) { return ''; }" +
            "})()",
            accountName -> {
                String name = accountName != null ? accountName.replace("\"", "") : "";
                if (name.isEmpty()) name = "Pengguna Google";
                finishLogin(cookie, name);
            }
        );
    }

    private void finishLogin(String cookie, String accountName) {
        // Simpan data login ke SharedPreferences
        SharedPreferences prefs = getSharedPreferences("auspoty_login", MODE_PRIVATE);
        prefs.edit()
            .putString("cookie", cookie)
            .putString("accountName", accountName)
            .putString("visitorData", visitorData)
            .putString("dataSyncId", dataSyncId)
            .putBoolean("isLoggedIn", true)
            .apply();

        // Kirim hasil ke MainActivity
        Intent result = new Intent();
        result.putExtra("accountName", accountName);
        result.putExtra("cookie", cookie);
        setResult(RESULT_OK, result);
        finish();
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            setResult(RESULT_CANCELED);
            super.onBackPressed();
        }
    }
}
