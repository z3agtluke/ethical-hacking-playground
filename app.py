import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.secret_key = "change-this-secret-for-production"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SESSION_PERMANENT"] = False


def get_db_connection():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the database tables and a default user if they do not exist."""
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    conn = get_db_connection()
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                comment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                filename TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        user = conn.execute("SELECT id FROM users WHERE username = ?", ("student",)).fetchone()
        if user is None:
            conn.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                ("student", "learn123", "student@example.local"),
            )
    conn.close()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def current_user():
    return session.get("username")


@app.before_first_request
def setup():
    init_db()


@app.route("/")
def index():
    if current_user():
        return redirect(url_for("profile"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
        conn.close()

        if user:
            session["username"] = user["username"]
            flash("Berhasil login. Selamat datang, {}!".format(username), "success")
            return redirect(url_for("profile"))

        flash("Username atau password salah. Coba lagi.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Anda telah logout.", "info")
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    username = current_user()
    if not username:
        return redirect(url_for("login"))

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    comment_count = conn.execute(
        "SELECT COUNT(*) FROM comments WHERE username = ?", (username,)
    ).fetchone()[0]
    uploads = conn.execute(
        "SELECT filename, uploaded_at FROM uploads WHERE username = ? ORDER BY uploaded_at DESC LIMIT 5",
        (username,),
    ).fetchall()
    conn.close()

    return render_template(
        "profile.html",
        user=user,
        comment_count=comment_count,
        uploads=uploads,
    )


@app.route("/comment", methods=["GET", "POST"])
def comment():
    username = current_user()
    if not username:
        return redirect(url_for("login"))

    conn = get_db_connection()
    if request.method == "POST":
        comment_text = request.form.get("comment", "").strip()
        if comment_text:
            conn.execute(
                "INSERT INTO comments (username, comment) VALUES (?, ?)",
                (username, comment_text),
            )
            conn.commit()
            flash("Komentar Anda sudah disimpan.", "success")
            return redirect(url_for("comment"))
        flash("Komentar tidak boleh kosong.", "warning")

    comments = conn.execute(
        "SELECT username, comment, created_at FROM comments ORDER BY created_at DESC LIMIT 20"
    ).fetchall()
    conn.close()
    return render_template("comment.html", comments=comments)


@app.route("/search", methods=["GET", "POST"])
def search():
    username = current_user()
    if not username:
        return redirect(url_for("login"))

    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            conn = get_db_connection()
            results = conn.execute(
                "SELECT username, comment, created_at FROM comments WHERE comment LIKE ? ORDER BY created_at DESC LIMIT 20",
                (f"%{query}%",),
            ).fetchall()
            conn.close()
            flash("Menampilkan hasil untuk: {}".format(query), "info")
        else:
            flash("Masukkan kata kunci pencarian.", "warning")

    return render_template("search.html", results=results, query=query)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    username = current_user()
    if not username:
        return redirect(url_for("login"))

    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("Pilih file untuk diupload.", "warning")
            return redirect(url_for("upload"))

        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            saved_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(saved_path)

            conn = get_db_connection()
            conn.execute(
                "INSERT INTO uploads (username, filename) VALUES (?, ?)",
                (username, filename),
            )
            conn.commit()
            conn.close()

            flash("Upload berhasil: {}".format(filename), "success")
            return redirect(url_for("upload"))

        flash("Jenis file tidak diperbolehkan. Gunakan txt, pdf, png, jpg, jpeg, atau gif.", "danger")

    conn = get_db_connection()
    uploads = conn.execute(
        "SELECT filename, uploaded_at FROM uploads ORDER BY uploaded_at DESC LIMIT 20"
    ).fetchall()
    conn.close()

    return render_template("upload.html", uploads=uploads)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
