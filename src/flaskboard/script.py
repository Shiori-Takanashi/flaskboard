# Use this command, print strings.
# docker build -t script .and
# docker run script


def output_hello() -> None:
    print("Hello, World!")


def main() -> None:
    output_hello()


if __name__ == "__main__":
    main()
