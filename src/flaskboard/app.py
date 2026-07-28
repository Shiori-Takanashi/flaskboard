import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL, text


db = SQLAlchemy()


def create_flask_app() -> Flask:
    load_dotenv(find_dotenv(".env.postgres"))

    load_dotenv(find_dotenv(".env.flask"))

    app = Flask(__name__)

    database_url = URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )
    print(os.environ["DB_HOST"])
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    db.init_app(app)

    return app


def connect_app_to_postgres(app: Flask) -> None:
    query = """
        SELECT version();
    """

    try:
        with app.app_context():
            with db.engine.connect() as connection:
                postgres_version = connection.execute(text(query)).scalar_one()

        print("データベース接続に成功しました。")
        print(f"PostgreSQLバージョン: {postgres_version}")

    except Exception as error:
        print(
            f"データベース接続に失敗しました。{type(error).__name__}: {error}"
        )
        raise


def run() -> Flask:
    print("Function: run")
    flask_app = create_flask_app()
    connect_app_to_postgres(flask_app)
    return flask_app


def main() -> None:
    print("Function: main")
    flask_app = create_flask_app()
    connect_app_to_postgres(flask_app)


if __name__ == "__main__":
    main()
