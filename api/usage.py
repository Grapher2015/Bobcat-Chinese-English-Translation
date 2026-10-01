"""Vercel Python Serverless Function: DeepL usage proxy.

GET /api/usage?auth_key=...
key 只在内存里转发给 DeepL，本函数不做任何持久化。
"""
from http.server import BaseHTTPRequestHandler
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qsl, urlencode

DEEPL_BASE = "https://api-free.deepl.com"


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

    def do_GET(self):
        qs = urlparse(self.path).query
        params = dict(parse_qsl(qs, keep_blank_values=True))
        auth_key = params.pop("auth_key", "")
        rest = urlencode(params)
        url = DEEPL_BASE + "/v2/usage" + ("?" + rest if rest else "")
        req = urllib.request.Request(url, headers={
            "Authorization": "DeepL-Auth-Key " + auth_key,
            "User-Agent": "vercel-deepl-proxy/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                status, body = r.status, r.read()
        except urllib.error.HTTPError as e:
            status, body = e.code, e.read()
        self._send(status, body)

    def log_message(self, *args):
        pass
