from pathlib import Path


def debug_function(
    a,
    b,
    c,
    d,
    e,
):
    result = a + b + c + d + e
    if result is None:
        return None
    else:
        return Path(__file__)


if __name__ == "__main__":
    p = debug_function(
        1,
        2,
        3,
        4,
        5,
    )
    print(p)
