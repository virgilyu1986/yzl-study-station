#!/usr/bin/env python3
"""学习能量站静态服务器：所有响应强制禁用缓存，确保 Safari 等浏览器每次都拿到最新版本。"""
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class NoCacheHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # 强制浏览器不缓存，每次访问都向服务器验证/拉取最新内容
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # 静默访问日志


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), NoCacheHandler)
    print(f"Serving {BASE_DIR} on 0.0.0.0:{port} (no-cache enabled)")
    server.serve_forever()
