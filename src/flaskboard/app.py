import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL, func, select, text


db = SQLAlchemy()


def build_database_url() -> URL:
    return URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )


def create_flask_app() -> Flask:
    load_dotenv(find_dotenv(".env.flask"))
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = build_database_url()

    db.init_app(app)

    return app


def get_postgres_version(app: Flask) -> str:
    with app.app_context():
        version = db.session.execute(select(func.version())).scalar_one()
        return str(version)


def connect_app_to_postgres(app: Flask) -> None:
    try:
        postgres_version = get_postgres_version(app)

        print("データベース接続に成功しました。")
        print(f"PostgreSQLバージョン: {postgres_version}")

    except Exception as error:
        print(
            f"データベース接続に失敗しました。{type(error).__name__}: {error}"
        )
        raise


def print_tasks(app: Flask) -> None:
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
            task_is_done = task.get("is_done")

            print(
                f"{task_id:02d}: {task_name} [{'完了' if task_is_done else '未完了'}]"
            )


def run() -> Flask:
    print("Function: run")
    flask_app = create_flask_app()
    connect_app_to_postgres(flask_app)
    print_tasks(flask_app)
    return flask_app


def main() -> None:
    print("Function: main")
    flask_app = create_flask_app()
    connect_app_to_postgres(flask_app)
    print_tasks(flask_app)


if __name__ == "__main__":
    main()
