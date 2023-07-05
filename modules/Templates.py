from core.modules.Base import Base
from api.TemplatesAPI import TemplatesAPI

from core.console import reptor_console
from utils.table import make_table


class Templates(Base):
    """
    Queries Server for Finding Templates


    Sample commands:
        reptor templates
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.arg_search = kwargs.get("search")

    @classmethod
    def add_arguments(cls, parser):
        super().add_arguments(parser)
        templates_parsers = parser.add_argument_group()
        templates_parsers.add_argument(
            "--search", help="Search for term", action="store", default=None
        )

    def run(self):
        template_api: TemplatesAPI = TemplatesAPI(self.reptor)
        if not self.arg_search:
            templates = template_api.get_templates()
        else:
            templates = template_api.search(self.arg_search)

        table = make_table(["Title", "ID"])
        for template in templates:
            finding = template.data
            if finding:
                table.add_row(finding.title, template.id)
            else:
                print(f"Template has no finding date.")

        reptor_console.print(table)


loader = Templates
