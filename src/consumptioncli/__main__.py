# stdlib
from sys import exit, stderr
from argparse import ArgumentError

# consumption
from consumptioncli.parsing import MainParser, BetterNamespace


def main() -> int:
    try:
        main_parser = MainParser.get()
        args = main_parser.parse_args(namespace=BetterNamespace())
        print(getattr(args, "handler")(args))
        return 0
    except ArgumentError as e:
        print(e.message, file=stderr)
        return 1


if __name__ == "__main__":
    exit(main())
