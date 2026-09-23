import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL


db = SQLAlchemy()

app = Flask(__name__)

url = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    database=os.environ["POSTGRES_DB"],
    host=os.environ["DATABASE_HOST_NAME"],
    port=int(os.environ["DATABASE_PORT"]),
)

app.config["SQLALCHEMY_DATABASE_URI"] = url

db.init_app(app)


@app.get("/")
def index() -> str:
    return "Flaskboard"
