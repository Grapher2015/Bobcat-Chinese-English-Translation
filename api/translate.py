"""Vercel Python Serverless Function: DeepL translate proxy.

POST /api/translate  { text, target_lang, source_lang?, auth_key }
key 只在内存里转发给 DeepL，本函数不做任何持久化。
"""
from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error

DEEPL_BASE = "https://api-free.deepl.com"


def _forward(req):
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


class handler(BaseHTTPRequestHandler):
    def _send(self, status, body):
        self.send_response(status)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            return self._send(400, b'{"ok": false, "error": "bad_request"}')
        auth_key = payload.pop("auth_key", "")
        if not auth_key or not str(payload.get("text", "")).strip():
            return self._send(400, b'{"ok": false, "error": "missing auth_key or text"}')
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            DEEPL_BASE + "/v2/translate", data=data, method="POST",
            headers={"Content-Type": "application/json",
                     "Authorization": "DeepL-Auth-Key " + auth_key,
                     "User-Agent": "vercel-deepl-proxy/1.0"})
        status, body = _forward(req)
        self._send(status, body)

    def log_message(self, *args):
        pass
