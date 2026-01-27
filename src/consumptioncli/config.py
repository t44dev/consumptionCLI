import json
import os
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, TypedDict

from consumptionbackend.utils import ServiceBase
from platformdirs import user_config_path, user_data_path, user_log_path

from consumptioncli.utils import ExtendedEncoder

CONSUMPTION_CONFIG_DIR = os.getenv("CONSUMPTION_CONFIG_DIR")
CONSUMPTION_DATA_DIR = os.getenv("CONSUMPTION_DATA_DIR")
CONSUMPTION_LOG_DIR = os.getenv("CONSUMPTION_LOG_DIR")


class Config(TypedDict):
    db_path: Path
    log_path: Path


class ConfigService(ServiceBase):
    CONIFG_PATH: Path = (
        user_config_path() / "consumption"
        if CONSUMPTION_CONFIG_DIR is None
        else Path(CONSUMPTION_CONFIG_DIR)
    ) / "config.json"
    DEFAULT_CONFIG: Config = {
        "db_path": (
            user_data_path() / "consumption"
            if CONSUMPTION_DATA_DIR is None
            else Path(CONSUMPTION_DATA_DIR)
        )
        / "consumption.db",
        "log_path": (
            user_log_path() / "consumption"
            if CONSUMPTION_LOG_DIR is None
            else Path(CONSUMPTION_LOG_DIR)
        )
        / "consumption.log",
    }

    def __init__(self) -> None:
        super().__init__()
        self._config: Config | None = None
        cls = self.__class__

        if not cls.CONIFG_PATH.is_file():
            cls.CONIFG_PATH.parent.mkdir(exist_ok=True, parents=True)
            self.write(cls.DEFAULT_CONFIG)

    def read(self) -> Config:
        if self._config is None:
            with open(self.CONIFG_PATH, "r") as file:
                config = json.load(file, object_hook=self.__class__.config_load_hook)
                self._config = config
                return config

        return self._config

    def write(self, config: Config) -> None:
        with open(self.CONIFG_PATH, "w+") as file:
            return json.dump(config, file, cls=ExtendedEncoder)

    @classmethod
    def config_load_hook(cls, d: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        d["db_path"] = Path(d["db_path"])
        d["log_path"] = Path(d["log_path"])
        return d
