import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, session, url_for


FINAL_FLAG = "FLAG{h1dd3n_1n_pl41n_s1ght_9f3a2c}"
CHALLENGE_USERNAME = "svc_backup"
CHALLENGE_PASSWORD = "password123"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "ctf.sqlite3"

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "training-room-dev-key-change-me")


TOP_LEVEL_PAGES = {
    "admin": {
        "title": "Administration Console",
        "summary": "Access review workspace for internal operations.",
        "links": [
            ("logs", "Log Extract"),
            ("users", "User Queue"),
        ],
    },
    "backup": {
        "title": "Backup Index",
        "summary": "Scheduled archive status for shared application systems.",
        "links": [
            ("daily", "Daily Snapshot"),
            ("restore", "Restore Notes"),
        ],
    },
    "config": {
        "title": "Configuration Service",
        "summary": "Deployment settings mirror for QA validation.",
        "links": [
            ("env", "Environment"),
            ("staging", "Staging Mirror"),
        ],
    },
    "dev": {
        "title": "Developer Holding Area",
        "summary": "Unreviewed engineering notes and temporary checks.",
        "links": [
            ("builds", "Build Results"),
            ("tickets", "Ticket Cache"),
        ],
    },
    "test": {
        "title": "Test Harness",
        "summary": "QA smoke records and temporary acceptance notes.",
        "links": [
            ("results", "Result Archive"),
            ("cases", "Case Matrix"),
        ],
    },
}


CHILD_PAGES = {
    ("admin", "logs"): {
        "title": "Administration Log Extract",
        "lines": [
            "2026-08-28 09:14:02 review job queued for account import",
            "2026-08-28 09:15:11 stale report removed from spool",
            "2026-08-28 09:17:43 permissions export completed",
        ],
    },
    ("admin", "users"): {
        "title": "Administration User Queue",
        "lines": [
            "Pending onboarding batch: 0",
            "Pending offboarding batch: 2",
            "Access exceptions require manager acknowledgement.",
        ],
    },
    ("backup", "daily"): {
        "title": "Daily Backup Snapshot",
        "lines": [
            "NAS-01: completed with warnings",
            "DB-REPORTING: completed",
            "QA-FILES: skipped by maintenance window",
        ],
    },
    ("backup", "restore"): {
        "title": "Restore Notes",
        "lines": [
            "Restore drill owner: infrastructure",
            "Last tabletop review: 2026-08-19",
            "No production restore request is approved from this panel.",
        ],
    },
    ("config", "env"): {
        "title": "Environment",
        "lines": [
            "APP_MODE=qa",
            "MAIL_RELAY=disabled",
            "EXTERNAL_API=stub",
        ],
    },
    ("config", "staging"): {
        "title": "Staging Mirror",
        "lines": [
            "Mirror health: degraded",
            "Sync owner: platform services",
            "Legacy notes retained for audit comparison.",
        ],
        "comment": "staging mirror moved: /hidden/",
    },
    ("dev", "builds"): {
        "title": "Build Results",
        "lines": [
            "corp-tools-api #1842: passed",
            "corp-tools-web #1843: failed lint threshold",
            "corp-tools-worker #1844: pending artifact cleanup",
        ],
    },
    ("dev", "tickets"): {
        "title": "Ticket Cache",
        "lines": [
            "DEV-2198: waiting on review",
            "DEV-2201: duplicate of DEV-2177",
            "DEV-2204: needs reproduction steps",
        ],
    },
    ("test", "results"): {
        "title": "Result Archive",
        "lines": [
            "Smoke suite: 71 passed, 3 skipped",
            "Regression suite: blocked by fixture refresh",
            "Manual acceptance: scheduled",
        ],
    },
    ("test", "cases"): {
        "title": "Case Matrix",
        "lines": [
            "Authentication: partial",
            "Reporting: not started",
            "Export workflow: needs sample data",
        ],
    },
}


FILLER_PAGES = {
    "about": {
        "title": "About",
        "body": "CorpTools supports routine internal workflow review and temporary QA activities.",
    },
    "contact": {
        "title": "Contact",
        "body": "Contact IT operations through the normal ticketing channel for all access requests.",
    },
    "services": {
        "title": "Services",
        "body": "Internal services listed here are subject to maintenance windows and audit review.",
    },
}


def db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        conn.execute("DELETE FROM users")
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (CHALLENGE_USERNAME, CHALLENGE_PASSWORD),
        )
        conn.commit()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/f")
def prank_step_f():
    return render_template(
        "breadcrumb.html",
        title="File Review",
        heading="File Review",
        comment="next review path: /f/l",
    )


@app.route("/f/l")
def prank_step_l():
    return render_template(
        "breadcrumb.html",
        title="Legacy File Review",
        heading="Legacy File Review",
        comment="next review path: /f/l/a",
    )


@app.route("/f/l/a")
def prank_step_a():
    return render_template(
        "breadcrumb.html",
        title="Archive File Review",
        heading="Archive File Review",
        comment="next review path: /f/l/a/g",
    )


@app.route("/f/l/a/g")
def prank_flag():
    return redirect("https://youtu.be/dQw4w9WgXcQ", code=302)


@app.route("/<page>")
def filler(page):
    if page in TOP_LEVEL_PAGES:
        return section_index(page)
    content = FILLER_PAGES.get(page)
    if content is None:
        abort(404)
    return render_template("filler.html", **content)


@app.route("/<section>/")
@app.route("/<section>")
def section_index(section):
    content = TOP_LEVEL_PAGES.get(section)
    if content is None:
        abort(404)
    return render_template("section.html", section=section, **content)


@app.route("/<section>/<child>")
def section_child(section, child):
    if section not in TOP_LEVEL_PAGES:
        abort(404)
    content = CHILD_PAGES.get((section, child))
    if content is None:
        abort(404)
    return render_template("child.html", section=section, child=child, **content)


@app.route("/hidden")
@app.route("/hidden/")
def hidden_index():
    return render_template("hidden_index.html")


@app.route("/hidden/notes")
def hidden_notes():
    return render_template("hidden_notes.html")


@app.route("/hidden/login", methods=["GET", "POST"])
def hidden_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        with db_connection() as conn:
            user = conn.execute(
                "SELECT username FROM users WHERE username = ? AND password = ?",
                (username, password),
            ).fetchone()
        if user:
            session["user"] = user["username"]
            return redirect(url_for("hidden_vault"))
        error = "invalid credentials"
    return render_template("hidden_login.html", error=error)


@app.route("/hidden/vault")
def hidden_vault():
    if not session.get("user"):
        return redirect(url_for("hidden_login"))
    return render_template("hidden_vault.html", flag=FINAL_FLAG)


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
