from argparse import ArgumentError
from sys import exit, stderr

from consumptionbackend.utils.exceptions import NoValuesError

from .parsing import BetterNamespace, MainParser, post_process


def main() -> int:
    try:
        main_parser = MainParser.get()
        args = main_parser.parse_args(namespace=BetterNamespace())
        args = post_process(args, getattr(args, "date_format"))
        print(getattr(args, "handler")(**args))
        return 0
    except (ArgumentError, NoValuesError) as e:
        print(e.message, file=stderr)
        return 1


if __name__ == "__main__":
    exit(main())
