# stdlib
from sys import exit, stderr
from argparse import ArgumentError

# consumption
from .parsing import MainParser, BetterNamespace, post_process


def main() -> int:
    try:
        main_parser = MainParser.get()
        args = main_parser.parse_args(namespace=BetterNamespace())
        args = post_process(args, getattr(args, "date_format"))
        print(getattr(args, "handler")(args))
        return 0
    except ArgumentError as e:
        print(e.message, file=stderr)
        return 1


if __name__ == "__main__":
    exit(main())
