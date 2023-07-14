import typing
from abc import abstractmethod

from reptor.lib.console import Console
from reptor.lib.logger import ReptorAdapter

from .conf import ConfigProtocol


class ReptorProtocol(typing.Protocol):
    logger: ReptorAdapter
    console: Console
    plugin_manager: typing.Any

    @abstractmethod
    def get_config(self) -> ConfigProtocol:
        ...
