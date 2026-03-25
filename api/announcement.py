from http.server import BaseHTTPRequestHandler
import json, imaplib, email, os
from email.header import decode_header

# ── Kredensial Gmail inbox yang dipantau ─────────────────────────────────────
IMAP_USER     = "yusrilrizky121@gmail.com"
IMAP_PASS     = "mhyjenewwghdkbow"   # App Password (tanpa spasi)
IMAP_HOST     = "imap.gmail.com"
ADMIN_EMAIL   = "yusrilrizky149@gmail.com"   # satu-satunya yang boleh kirim
# ─────────────────────────────────────────────────────────────────────────────

# In-memory store untuk announcement yang dikirim via POST (admin panel)
# Di Vercel serverless, ini akan reset tiap cold start — tapi cukup untuk notifikasi
_manual_announcement = {}

def _decode_str(s):
    if s is None:
        return ""
    parts = decode_header(s)
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(part)
    return "".join(result)

def _get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get("Content-Disposition", ""))
            if ct == "text/plain" and "attachment" not in cd:
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="replace").strip()
    else:
        charset = msg.get_content_charset() or "utf-8"
        return msg.get_payload(decode=True).decode(charset, errors="replace").strip()
    return ""

def fetch_latest_announcement():
    """Coba ambil dari manual store dulu, fallback ke IMAP."""
    global _manual_announcement
    if _manual_announcement.get("status") == "success":
        return _manual_announcement
    if _manual_announcement.get("status") == "none":
        return {"status": "none"}
    # Fallback: baca dari Gmail IMAP
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, 993)
        mail.login(IMAP_USER, IMAP_PASS)
        mail.select("INBOX")
        status, data = mail.search(None, f'FROM "{ADMIN_EMAIL}"')
        if status != "OK" or not data[0]:
            mail.logout()
            return None
        ids = data[0].split()
        latest_id = ids[-1]
        status, msg_data = mail.fetch(latest_id, "(RFC822)")
        mail.logout()
        if status != "OK":
            return None
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        subject = _decode_str(msg.get("Subject", "Auspoty"))
        body    = _get_body(msg)
        msg_id  = msg.get("Message-ID", latest_id.decode())
        lower = (subject + body).lower()
        if any(w in lower for w in ["update", "versi", "version", "rilis"]):
            ann_type = "update"
        elif any(w in lower for w in ["peringatan", "warning", "penting", "urgent"]):
            ann_type = "warning"
        elif any(w in lower for w in ["promo", "diskon", "gratis", "free"]):
            ann_type = "promo"
        else:
            ann_type = "info"
        return {
            "status":  "success",
            "id":      str(msg_id).strip(),
            "title":   subject[:100] if subject.strip() else (body[:60] + "...") or "Pesan dari Admin",
            "message": body[:500] if body else subject or "Ada pesan baru dari admin.",
            "type":    ann_type,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def _cors_headers(handler_self, code=200, methods="GET, POST, OPTIONS"):
    handler_self.send_response(code)
    handler_self.send_header("Content-Type", "application/json")
    handler_self.send_header("Access-Control-Allow-Origin", "*")
    handler_self.send_header("Access-Control-Allow-Methods", methods)
    handler_self.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler_self.end_headers()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        result = fetch_latest_announcement()
        if result is None:
            result = {"status": "none"}
        _cors_headers(self)
        self.wfile.write(json.dumps(result).encode())

    def do_POST(self):
        global _manual_announcement
        try:
            length = int(self.headers.get("Content-Length", 0))
            body   = self.rfile.read(length)
            data   = json.loads(body)
        except Exception:
            _cors_headers(self, 400)
            self.wfile.write(json.dumps({"status": "error", "message": "Invalid JSON"}).encode())
            return

        # Validasi admin
        if data.get("adminEmail") != ADMIN_EMAIL:
            _cors_headers(self, 403)
            self.wfile.write(json.dumps({"status": "error", "message": "Unauthorized"}).encode())
            return

        status  = data.get("status", "none")
        title   = str(data.get("title", "")).strip()[:100]
        message = str(data.get("message", "")).strip()[:500]
        ann_id  = str(data.get("id", "")).strip()
        ann_type = data.get("type", "info")

        if status == "none":
            # Hapus pengumuman aktif
            _manual_announcement = {"status": "none"}
            _cors_headers(self)
            self.wfile.write(json.dumps({"status": "ok", "message": "Pengumuman dihapus"}).encode())
            return

        if not title or not message:
            _cors_headers(self, 400)
            self.wfile.write(json.dumps({"status": "error", "message": "Judul dan pesan wajib diisi"}).encode())
            return

        _manual_announcement = {
            "status":  "success",
            "id":      ann_id or str(hash(title + message)),
            "title":   title,
            "message": message,
            "type":    ann_type,
        }
        _cors_headers(self)
        self.wfile.write(json.dumps({"status": "ok", "message": "Pengumuman berhasil dikirim"}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        pass
