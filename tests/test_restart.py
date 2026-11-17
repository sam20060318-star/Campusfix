"""TC04 end to end: start the real server process, stop it, start it again.

Uses only the standard library to talk to the server over HTTP.
"""

import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from http.cookiejar import CookieJar
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def start_server(db_file, port):
    env = {**os.environ, "CAMPUSFIX_DB": str(db_file)}
    process = subprocess.Popen(
        [sys.executable, str(ROOT / "app.py"), "--port", str(port)],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(100):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/api/reports", timeout=1).close()
            return process
        except OSError:
            time.sleep(0.1)
    process.kill()
    raise RuntimeError("server did not start")


def stop_server(process):
    process.terminate()
    process.wait(timeout=10)


def call(opener, method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    with opener.open(request, timeout=5) as response:
        return json.loads(response.read())


def test_tc04_real_process_restart_keeps_report_status_and_note(tmp_path):
    db_file = tmp_path / "campusfix.db"
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))

    server = start_server(db_file, port)
    try:
        report = call(opener, "POST", f"{base}/api/reports", {
            "title": "Broken hallway light", "location": "Building B",
            "category": "Facilities", "description": "The light is not working.",
        })
        call(opener, "POST", f"{base}/api/login", {"username": "staff", "password": "staff123"})
        call(opener, "PATCH", f"{base}/api/reports/{report['id']}/status",
             {"status": "Resolved", "resolution_note": "The light bulb was replaced."})
    finally:
        stop_server(server)

    server = start_server(db_file, port)
    try:
        saved = call(opener, "GET", f"{base}/api/reports/{report['id']}")
        assert saved["title"] == "Broken hallway light"
        assert saved["location"] == "Building B"
        assert saved["status"] == "Resolved"
        assert saved["resolution_note"] == "The light bulb was replaced."
        # The staff session also survives the restart (secret key is stored beside the database).
        assert call(opener, "GET", f"{base}/api/me")["role"] == "staff"
    finally:
        stop_server(server)
