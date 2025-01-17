import typing
from posixpath import join as urljoin

from reptor.api.APIClient import APIClient
from reptor.models.FindingTemplate import FindingTemplate


class TemplatesAPI(APIClient):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_endpoint = urljoin(
            self.reptor.get_config().get_server(), f"api/v1/findingtemplates/"
        )

    def get_template_overview(self) -> typing.List[FindingTemplate]:
        """Gets list of Templates"""
        response = self.get(self.base_endpoint)
        return_data = list()
        for item in response.json()["results"]:
            return_data.append(FindingTemplate(item))
        return return_data

    def get_template(self, template_id: str) -> FindingTemplate:
        """Gets a single Template by ID"""
        response = self.get(urljoin(self.base_endpoint, template_id))
        return FindingTemplate(response.json())

    def export(self, template_id: str) -> bytes:
        """Exports a template in archive format (tar.gz)"""
        url = urljoin(self.base_endpoint, f"{template_id}/export/")
        return self.post(url).content

    def search(
        self, search_term, deduplicate: bool = True
    ) -> typing.List[FindingTemplate]:
        """Searches through the templates"""

        response = self.get(urljoin(self.base_endpoint, f"?search={search_term}"))
        return_data = list()
        added_ids = set()
        for item in response.json()["results"]:
            finding_template = FindingTemplate(item)
            if finding_template.id not in added_ids:
                return_data.append(FindingTemplate(item))
            if deduplicate:
                added_ids.add(finding_template.id)
        return return_data

    def get_templates_by_tag(self, tag: str) -> typing.List[FindingTemplate]:
        matched_templates = list()
        for finding_template in self.search(tag):
            if tag in finding_template.tags:
                matched_templates.append(finding_template)
        return matched_templates

    def upload_template(self, template: FindingTemplate) -> FindingTemplate:
        """Uploads a new Finding Template to API

        Args:
            template (FindingTemplate): Model Data to upload

        Returns:
            FindingTemplate: Updated Model with ID etc.
        """
        create_template = True
        response_templates = self.get(self.base_endpoint)
        #print(response_templates.json()["results"])
        for t in response_templates.json()["results"]:
            if t["translations"][0]["data"]["title"] == template.translations[0].data.title:
                create_template = False
                break
        if create_template:
            res = self.post(
                self.base_endpoint,
                json=template.to_dict(),
            )
            return FindingTemplate(res.json())
        else:
            return None

    def delete_template(self, template_id: str) -> None:
        """Deletes a Template by ID"""
        self.delete(urljoin(self.base_endpoint, template_id))
        return
