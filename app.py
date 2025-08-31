from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change in production


# ---------------- DB SETUP ----------------
def init_sqlite_db():
    conn = sqlite3.connect("foodrescue.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        email TEXT UNIQUE,
                        password TEXT,
                        role TEXT,
                        location TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS donations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        donor_id INTEGER,
                        food_item TEXT,
                        quantity TEXT,
                        expiry_time TEXT,
                        status TEXT DEFAULT 'available',
                        FOREIGN KEY(donor_id) REFERENCES users(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS claims (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        donation_id INTEGER,
                        receiver_id INTEGER,
                        claim_time TEXT,
                        status TEXT DEFAULT 'pending',
                        FOREIGN KEY(donation_id) REFERENCES donations(id),
                        FOREIGN KEY(receiver_id) REFERENCES users(id)
                    )''')

    conn.commit()
    conn.close()


# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = generate_password_hash(request.form["password"])
        role = request.form["role"]
        location = request.form["location"]

        conn = sqlite3.connect("foodrescue.db")
        cursor = conn.cursor()

        # Check username separately
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("⚠️ Username already exists!", "danger")
            conn.close()
            return redirect(url_for("register"))

        # Check email separately
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_email = cursor.fetchone()

        if existing_email:
            flash("⚠️ Email already registered!", "danger")
            conn.close()
            return redirect(url_for("register"))

        # Insert new user
        cursor.execute("INSERT INTO users (username, email, password, role, location) VALUES (?, ?, ?, ?, ?)",
                       (username, email, password, role, location))
        conn.commit()
        conn.close()

        flash("✅ Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        conn = sqlite3.connect("foodrescue.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[4]

            if user[4] == "donor":
                return redirect(url_for("donor_dashboard"))
            else:
                return redirect(url_for("receiver_dashboard"))
        else:
            flash("❌ Invalid email or password!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/donor_dashboard", methods=["GET", "POST"])
def donor_dashboard():
    if "user_id" not in session or session["role"] != "donor":
        return redirect(url_for("login"))

    conn = sqlite3.connect("foodrescue.db")
    cursor = conn.cursor()

    if request.method == "POST":
        food_item = request.form["food_item"]
        quantity = request.form["quantity"]
        expiry_time = request.form["expiry_time"]

        cursor.execute("INSERT INTO donations (donor_id, food_item, quantity, expiry_time) VALUES (?, ?, ?, ?)",
                       (session["user_id"], food_item, quantity, expiry_time))
        conn.commit()
        flash("✅ Donation added successfully!", "success")

    cursor.execute("SELECT * FROM donations WHERE donor_id=?", (session["user_id"],))
    donations = cursor.fetchall()
    conn.close()

    return render_template("donor_dashboard.html", donations=donations)


@app.route("/receiver_dashboard")
def receiver_dashboard():
    if "user_id" not in session or session["role"] != "receiver":
        return redirect(url_for("login"))

    conn = sqlite3.connect("foodrescue.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donations WHERE status='available'")
    donations = cursor.fetchall()
    conn.close()

    return render_template("receiver_dashboard.html", donations=donations)


@app.route("/claim/<int:donation_id>")
def claim(donation_id):
    if "user_id" not in session or session["role"] != "receiver":
        return redirect(url_for("login"))

    conn = sqlite3.connect("foodrescue.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE donations SET status='claimed' WHERE id=?", (donation_id,))
    cursor.execute("INSERT INTO claims (donation_id, receiver_id, claim_time) VALUES (?, ?, datetime('now'))",
                   (donation_id, session["user_id"]))
    conn.commit()
    conn.close()

    flash("✅ Donation claimed successfully!", "success")
    return redirect(url_for("receiver_dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    flash("👋 You have logged out.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_sqlite_db()
    app.run(debug=True)
