from flask import Flask
from app.Command.MakeModel import make_model
from flask_migrate import Migrate
from app.Database.database import db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# -----------------------------
# DATABASE CONFIG (DYNAMIC)
# -----------------------------
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


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


if __name__ == "__main__":
    app.run(debug=True)