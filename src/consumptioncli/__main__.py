from argparse import ArgumentError
from sys import exit, stderr

from consumptionbackend.database.sqlite import register_sqlite_services
from consumptionbackend.utils import ServiceProvider
from consumptionbackend.utils.exceptions import NoValuesError

from consumptioncli.config import ConfigService
from consumptioncli.logging import setup_logging

from .parsing import BetterNamespace, MainParser, post_process


def main() -> int:
    # Services
    ServiceProvider.register(ConfigService, ConfigService())
    register_sqlite_services(ServiceProvider.get(ConfigService).read()["db_path"])
    setup_logging(ServiceProvider.get(ConfigService).read()["log_path"])

    # Parsing
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
