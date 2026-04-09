from flask import Flask, render_template
from app.Command.MakeModel import make_model
from flask_migrate import Migrate
from app.Database.database import db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder="app/Resources/assets", template_folder="app/Resources/view")

# -----------------------------
# DATABASE CONFIG (DYNAMIC)
# -----------------------------
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")

app.config["SQLALCHEMY_DATABASE_URI"] = (f"{DB_DRIVER}+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")


# -----------------------------
# INIT
# -----------------------------
db.init_app(app)
migrate = Migrate(app, db, directory="app/Database/Migrations")


# -----------------------------
# INIT
# -----------------------------
from app import Models


# -----------------------------
# LOAD MODELS
# -----------------------------
app.cli.add_command(make_model)

@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    return render_template("index.html")

@app.route("/sign-up", methods=["GET"], strict_slashes=False)
def sign_up():
    return render_template("sign-up.html")

@app.route("/sign-in", methods=["GET"], strict_slashes=False)
def sign_in():
    return render_template("sign-in.html")

@app.route("/tables", methods=["GET"], strict_slashes=False)
def tables():
    return render_template("tables.html")

@app.route("/basic-forms", methods=["GET"], strict_slashes=False)
def basic_forms():
    return render_template("basic-forms.html")

@app.route("/form-layouts", methods=["GET"], strict_slashes=False)
def form_layouts():
    return render_template("form-layouts.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
