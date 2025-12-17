from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import os
from src.predict import predict_image

app = Flask(__name__)
app.secret_key = "melanoma_secret_key"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- DATABASE ----------------
def get_db():
    return sqlite3.connect("users.db")

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )
        user = cur.fetchone()

        if user:
            session["user"] = email
            return redirect("/home")
        else:
            flash("User not registered. Please register first.")

    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        age = request.form.get("age")
        dob = request.form.get("dob")

        db = get_db()
        db.execute(
            "INSERT INTO users (name, email, password, age, dob) VALUES (?,?,?,?,?)",
            (name, email, password, age, dob)
        )
        db.commit()

        return redirect("/")

    return render_template("register.html")

# ---------------- HOME ----------------
@app.route("/home", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/")

    result = None
    advice = None
    confidence = None
    image_path = None
    css = None

    if request.method == "POST":
        image = request.files.get("image")

        if image and image.filename != "":
            image_path = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(image_path)

            pred = predict_image(image_path)
            confidence = round(pred * 100, 2)

    

            if pred < 0.30:
                result = "🟢 Low Risk"
                advice = "Lesion appears likely benign. Continue regular skin checks."
                css = "low"

            elif pred < 0.60:
                result = "🟡 Medium Risk"
                advice = "Uncertain result. Monitor changes and consider medical advice."
                css = "medium"

            else:
                result = "🔴 High Risk"
                advice = "High risk detected. Please consult a dermatologist immediately."
                css = "high"


    return render_template(
        "home.html",
        result=result,
        advice=advice,
        confidence=confidence,
        image=image_path,
        css=css
    )

# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT name, email, age, dob FROM users WHERE email=?",
        (session["user"],)
    )
    data = cur.fetchone()

    user = {
        "name": data[0],
        "email": data[1],
        "age": data[2],
        "dob": data[3]
    }

    return render_template("profile.html", user=user)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
