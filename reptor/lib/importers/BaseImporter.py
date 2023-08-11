import typing

from reptor.api.models import FindingDataRaw, FindingTemplate
from reptor.lib.interfaces.reptor import ReptorProtocol
from reptor.lib.plugins.Base import Base


class BaseImporter(Base):
    reptor: ReptorProtocol
    mapping: typing.Dict
    meta: typing.Dict = {
        "name": "",
        "author": "",
        "version": "",
        "website": "",
        "license": "",
        "tags": [],
        "summary": "",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reptor = kwargs.get("reptor", None)
        self.finding_language = kwargs.get("language", "en-US")
        self.tags = list(filter(None, (kwargs.get("tags") or "").split(",")))
        self.tags.append(f"{self.__class__.__name__.lower()}:imported")

    @classmethod
    def add_arguments(cls, parser, plugin_filepath=None):
        action_group = parser.add_argument_group()
        action_group.title = "Global Importer Settings"
        action_group.add_argument(
            "-tags",
            "--tags",
            action="store",
            help="Comma-separated tags for new templates",
        )

    def next_findings_batch(self) -> typing.List[typing.Dict]:
        """Implement this to yield the next findings to process"""
        raise NotImplementedError(
            "next_findings_batch not implemented in importer plugin"
        )

    def _create_finding_item(self, raw_data: typing.Dict) -> FindingTemplate:
        remapped_data = dict()
        for key, value in self.mapping.items():
            try:
                converted_data = raw_data[key]
            except KeyError:
                continue
            # check if we have a convert_method and call it
            # update the value
            convert_method_name = f"convert_{key}"
            if hasattr(self, convert_method_name):
                if callable(getattr(self, convert_method_name)):
                    converter_method = getattr(self, convert_method_name)
                    self.debug(f"Calling: {convert_method_name}")
                    converted_data = converter_method(raw_data[key])

            # get type of converted data. the real type. not data type "type"
            remapped_data.setdefault(value, type(converted_data)())
            if isinstance(converted_data, str):
                if remapped_data[value]:
                    remapped_data[value] += "\n"
                remapped_data[value] += converted_data
            elif isinstance(converted_data, dict):
                remapped_data.update(converted_data)
            else:
                remapped_data[value] += converted_data

        new_finding = FindingTemplate(remapped_data)
        new_finding.data = FindingDataRaw(remapped_data)
        return new_finding

    def _upload_finding_templates(self, new_finding: FindingTemplate):
        updated_template = self.reptor.api.templates.upload_new_template(
            new_finding, language=self.finding_language, tags=self.tags
        )
        if updated_template:
            self.display(f"Uploaded {updated_template.id}")
        else:
            self.error("Cancel? [Y/n]")
            abort_answer = input()[:1].lower()
            if abort_answer != "n":
                raise AssertionError("Cancelling")

    def run(self):
        try:
            self.mapping
        except AttributeError as e:
            raise AttributeError("Importer plugin does not define a mapping") from e

        for external_finding in self.next_findings_batch():  # type: ignore
            new_finding = self._create_finding_item(external_finding)
            if not new_finding:
                continue
            self.display(f'Uploading "{new_finding.data.title}"')
            self.debug(new_finding)
            self._upload_finding_templates(new_finding)
