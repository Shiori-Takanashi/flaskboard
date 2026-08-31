import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL, text


def create_flask_alchemy() -> SQLAlchemy:
    return SQLAlchemy()


def create_flask_app(db: SQLAlchemy) -> Flask:

    app = Flask(__name__)

    load_dotenv(find_dotenv(".env.flask"))

    url = URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = url

    db.init_app(app)

    return app


def check_connection(app: Flask, db: SQLAlchemy) -> None:
    try:
        with app.app_context():
            with db.engine.connect:
                pass
        print("データベース接続に成功しました。")

    except Exception as error:
        print(
            f"データベース接続に失敗しました。{type(error).__name__}: {error}"
        )
        raise


def execute_query(app: Flask, db: SQLAlchemy) -> None:
    query = text(
        """
        SELECT *
        FROM tasks
        ORDER BY id;
        """
    )

    with app.app_context():
        tasks = db.session.execute(query).mappings()

        for task in tasks:
            task_id = task.get("id")
            task_name = task.get("name")
            print(f"{task_id:02d}: {task_name}")


def main() -> Flask:
    db = create_flask_alchemy()
    print("create_flask_alchemy関数が完了")
    app = create_flask_app(db)
    print("create_flask_app関数が終了")
    check_connection(app, db)
    print("check_connection関数が終了")
    execute_query(app, db)
    print("excute_query関数が終了")
    return app
