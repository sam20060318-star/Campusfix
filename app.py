"""CampusFix: Flask app serving the student page, the staff page and the JSON API."""

import argparse
import os
import secrets
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, session
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash

import db

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB = BASE_DIR / "instance" / "campusfix.db"
MAX_LENGTHS = {"title": 120, "location": 80, "category": 60, "description": 2000}
MAX_NOTE_LENGTH = 1000
FIELD_LABELS = {"title": "標題", "location": "地點", "category": "分類", "description": "問題描述"}


def _secret_key(directory):
    """Keep sessions valid across restarts without committing a secret to Git."""
    if os.environ.get("CAMPUSFIX_SECRET_KEY"):
        return os.environ["CAMPUSFIX_SECRET_KEY"]
    key_file = Path(directory) / "secret_key"
    if not key_file.exists():
        key_file.write_text(secrets.token_hex(32), encoding="utf-8")
    return key_file.read_text(encoding="utf-8").strip()


# Jira CF-4｜S1 提交問題回報
def validate_report(body):
    """Server-side validation of the four required fields (CF S1)."""
    values, errors = {}, {}
    for field in db.REPORT_FIELDS:
        raw = body.get(field) if isinstance(body, dict) else None
        value = " ".join(raw.split()) if isinstance(raw, str) and field != "description" else raw
        value = value.strip() if isinstance(value, str) else ""
        if not value:
            errors[field] = f"請輸入{FIELD_LABELS[field]}。"
        elif len(value) > MAX_LENGTHS[field]:
            errors[field] = f"{FIELD_LABELS[field]}請勿超過 {MAX_LENGTHS[field]} 個字。"
        values[field] = value
    return values, errors


def create_app(db_path=None):
    app = Flask(__name__)
    app.json.ensure_ascii = False  # show Chinese messages as-is in JSON
    db_path = str(db_path or os.environ.get("CAMPUSFIX_DB") or DEFAULT_DB)
    db.init_db(db_path)
    app.config.update(
        DB_PATH=db_path,
        SECRET_KEY=_secret_key(Path(db_path).parent),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        MAX_CONTENT_LENGTH=1024 * 1024,
    )

    def error(status, message, **extra):
        return jsonify({"error": message, **extra}), status

    def current_user():
        """The role always comes from the server-side account, never from the request."""
        username = session.get("username")
        return db.get_user(db_path, username) if username else None

    def staff_required(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            user = current_user()
            if user is None:
                return error(401, "請先以 Staff 帳號登入。")
            if user["role"] != "staff":
                return error(403, "只有 Staff 可以更新報修。")
            return view(*args, **kwargs)
        return wrapper

    # ---------- Pages ----------

    @app.get("/")
    def student_page():
        return render_template("index.html")

    @app.get("/login")
    def login_page():
        return render_template("login.html", forbidden=False)

    @app.get("/staff")
    def staff_page():
        user = current_user()
        if user is None:
            return redirect("/login")
        if user["role"] != "staff":
            return render_template("login.html", forbidden=True, username=user["username"]), 403
        return render_template("staff.html", username=user["username"])

    # ---------- Report API (S1, S2, S3, S7, S8) ----------

    # Jira CF-4｜S1 提交問題回報
    @app.post("/api/reports")
    def create_report():
        body = request.get_json(silent=True)
        if not isinstance(body, dict):
            return error(400, "請送出有效的報修資料。")
        values, errors = validate_report(body)
        if errors:
            first = next(errors[field] for field in db.REPORT_FIELDS if field in errors)
            return error(400, first, errors=errors)
        return jsonify(db.create_report(db_path, values)), 201

    # Jira CF-5｜S2 查看報修列表
    @app.get("/api/reports")
    def list_reports():
        keyword = request.args.get("keyword", "")
        location = request.args.get("location", "")
        return jsonify(db.list_reports(db_path, keyword, location))

    # Jira CF-6｜S3 查看報修詳情與狀態
    @app.get("/api/reports/<int:report_id>")
    def get_report(report_id):
        report = db.get_report(db_path, report_id)
        return jsonify(report) if report else error(404, "找不到這筆報修。")

    @app.get("/api/locations")
    def list_locations():
        return jsonify(db.list_locations(db_path))

    # ---------- Staff API (S5, S6, S9) ----------

    @app.patch("/api/reports/<int:report_id>/status")
    @staff_required
    def update_status(report_id):
        body = request.get_json(silent=True)
        if not isinstance(body, dict):
            return error(400, "請送出有效的狀態更新。")
        status = body.get("status")
        if status not in db.STATUSES:
            return error(400, "狀態必須是 Submitted、In Progress 或 Resolved。")
        note = body.get("resolution_note")
        note = note.strip() if isinstance(note, str) else ""
        if status == "Resolved":
            if not note:
                return error(400, "結案時必須填寫處理備註。")
            if len(note) > MAX_NOTE_LENGTH:
                return error(400, f"處理備註請勿超過 {MAX_NOTE_LENGTH} 個字。")
        else:
            note = ""  # a report that is not resolved has no resolution note
        report = db.update_status(db_path, report_id, status, note)
        return jsonify(report) if report else error(404, "找不到這筆報修。")

    # ---------- Authentication (S9) ----------

    @app.post("/api/login")
    def login():
        body = request.get_json(silent=True)
        username = body.get("username") if isinstance(body, dict) else None
        password = body.get("password") if isinstance(body, dict) else None
        user = db.get_user(db_path, username.strip()) if isinstance(username, str) else None
        if not user or not isinstance(password, str) or not check_password_hash(user["password_hash"], password):
            return error(401, "帳號或密碼錯誤。")
        session.clear()
        session["username"] = user["username"]
        return jsonify({"username": user["username"], "role": user["role"]})

    @app.post("/api/logout")
    def logout():
        session.clear()
        return jsonify({"ok": True})

    @app.get("/api/me")
    def me():
        user = current_user()
        if user is None:
            return jsonify({"authenticated": False})
        return jsonify({"authenticated": True, "username": user["username"], "role": user["role"]})

    # ---------- Errors ----------

    @app.errorhandler(HTTPException)
    def http_error(exc):
        if request.path.startswith("/api/"):
            message = "找不到這個網址。" if exc.code == 404 else exc.description or exc.name
            return error(exc.code, message)
        return exc

    @app.after_request
    def no_store(response):
        # Always show the latest saved status instead of a cached copy.
        if request.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        return response

    return app


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run CampusFix locally.")
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "5000")))
    parser.add_argument("--seed-demo", action="store_true",
                        help="add three fictional reports if the database has none, then start")
    args = parser.parse_args(argv)
    app = create_app()
    if args.seed_demo:
        added = db.seed_demo_reports(app.config["DB_PATH"])
        print(f"示範資料：已加入 {added} 筆虛構報修。" if added else "示範資料：資料庫已有報修，未加入任何資料。")
    print(f"資料庫位置：{app.config['DB_PATH']}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
