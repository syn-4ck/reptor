import typing
from abc import abstractmethod

from .base import BaseApiProtocol


class ApiTemplatesProtocol(BaseApiProtocol):
    project_id: str

    @abstractmethod
    def upload_new_template(
        self, template: object, language: str, tags: typing.Optional[list] = None
    ):
        ...
