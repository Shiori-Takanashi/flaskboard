from flaskboard.greeting import hello


def test_hello() -> None:
    assert hello() == "Hello, World!"
