import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", page_title="Home")


@app.route("/phones")
def phones():
    return render_template("phones.html", page_title="Phones")


@app.route("/tablets")
def tablets():
    return render_template("tablets.html", page_title="Tablets")


@app.route("/laptops")
def laptops():
    return render_template("laptops.html", page_title="Laptops")


@app.route("/accessories")
def accessories():
    return render_template("accessories.html", page_title="Accessories")


@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact Us")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = existing_user["first_name"].lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", first_name=session["user"]))
            else:
                flash("Incorrect Email Address and/or Password")
                return redirect(url_for("sign_in"))

        else:
            flash("Incorrect Email Address and/or Password")
            return redirect(url_for("sign_in"))

    return render_template("sign_in.html", page_title="Sign In")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("Email already registered")
            return redirect(url_for("sign_up"))

        if request.form.get("password") != request.form.get("confirm_password"):
            flash("Passwords do not match")
            return redirect(url_for("sign_up"))

        sign_up = {
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(sign_up)

        session["user"] = request.form.get("first_name").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", first_name=session["user"]))

    return render_template("sign_up.html", page_title="Sign Up")


@app.route("/profile/<first_name>", methods=["GET", "POST"])
def profile(first_name):
    first_name = session["user"]

    if session["user"]:
        return render_template("profile.html", first_name=first_name, page_title="My Account")

    return redirect(url_for("sign_in"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("sign_in"))


app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
