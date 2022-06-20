from __future__ import annotations

import logging
from typing import Optional


class Logger(logging.Logger):
    __instance__: Optional[Logger] = None
    __TIME_FORMAT__: str = '%Y-%m-%d %H:%M:%S'
    __LOG_FORMAT__: str = '%(asctime)s.%(msecs)03d %(levelname)5s %(process)d --- ' \
                          '%(name)s [%(filename)-10s] %(message)s'

    def __new__(cls, *_, **__) -> Logger:
        if cls.__instance__ is None:
            cls.__instance__ = logging.getLogger('video.wall')
            cls.__instance__.setLevel(cls._log_level())
            cls.__instance__.addHandler(cls._handler())
        return cls.__instance__

    @staticmethod
    def _log_level() -> int:
        return logging.getLevelName('INFO')

    @classmethod
    def _handler(cls) -> logging.StreamHandler:
        _handler = logging.StreamHandler()
        _handler.setFormatter(cls._formatter())
        return _handler

    @staticmethod
    def _formatter() -> logging.Formatter:
        return logging.Formatter(
            fmt=Logger.__LOG_FORMAT__,
            datefmt=Logger.__TIME_FORMAT__
        )


logger = Logger()
