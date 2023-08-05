import typing
from abc import abstractmethod


class ConfigProtocol(typing.Protocol):
    @abstractmethod
    def get_config_from_user(self):
        ...

    @abstractmethod
    def get(
        self, key: str, default: typing.Optional[typing.Any] = None, plugin: str = ""
    ) -> typing.Any:
        ...

    @abstractmethod
    def get_config_keys(self, plugin: str = "") -> typing.Collection:
        ...

    @abstractmethod
    def store_config(self):
        ...

    @abstractmethod
    def set(self, key: str, value: typing.Any, plugin: str = "") -> None:
        ...

    @abstractmethod
    def get_server(self) -> str:
        ...

    @abstractmethod
    def get_token(self) -> str:
        ...

    @abstractmethod
    def get_project_id(self) -> str:
        ...

    @abstractmethod
    def get_cli_overwrite(self) -> typing.Dict:
        ...

    @abstractmethod
    def get_community_enabled(self) -> bool:
        ...
