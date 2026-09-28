import os

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL, String, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# 1. モデルの基底クラス
class Base(DeclarativeBase):
    pass


# 2. Base を Flask-SQLAlchemy に渡す
db = SQLAlchemy(model_class=Base)

# 3. Flask アプリと接続設定
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
app.config["TEMPLATES_AUTO_RELOAD"] = True

# 4. 設定済みのアプリに拡張を登録
db.init_app(app)
migrate = Migrate(app, db)


# 5. モデル
class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))


# 6. ルート
@app.get("/posts")
def get_posts() -> str:
    columns = inspect(db.engine).get_columns(Post.__tablename__)
    return render_template("posts.html", columns=columns)
