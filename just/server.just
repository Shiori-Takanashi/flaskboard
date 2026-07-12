# just/server.just

FLASK-PORT := "8000"
GUNICORN-PORT := "8080"
WORKERS := "2"
MODULE := "flaskboard.app:app"

f-server:
    uv run flask --app {{MODULE}} run --debug --host=0.0.0.0 --port={{FLASK-PORT}}

g-server:
    uv run gunicorn {{MODULE}} -w {{WORKERS}} -b 0.0.0.0:{{GUNICORN-PORT}}
