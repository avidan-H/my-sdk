from pathlib import Path
from typing import List, Optional

from TestSuite.integration import Integration
from TestSuite.json_based import JSONBased
from TestSuite.script import Script
from TestSuite.secrets import Secrets
from TestSuite.text_based import TextBased


class Pack:
    """A class that mocks a pack inside to content repo

    Note:
        Do not include the `self` parameter in the ``Args`` section.

    Args:
        packs_dir: A Path to the root of Packs dir
        name: name of the pack to create

    Attributes:
        path (str): A path to the content pack.
        secrets (Secrets): Exception error code.
        integrations: A list contains any created integration
        scripts:  A list contains any created Script

    """

    def __init__(self, packs_dir: Path, name: str, repo):
        # Initiate lists:
        self._repo = repo
        self.repo_path = repo.path
        self.integrations: List[Integration] = list()
        self.scripts: List[Script] = list()
        self.classifiers: List[JSONBased] = list()
        self.mapper: List[JSONBased] = list()
        self.dashboards: List[JSONBased] = list()
        self.incident_types: List[JSONBased] = list()
        self.incident_field: List[JSONBased] = list()
        self.indicator_field: List[JSONBased] = list()
        self.indicator_type: List[JSONBased] = list()
        self.layouts: List[JSONBased] = list()
        self.release_notes: List[TextBased] = list()

        # Create base pack
        self._pack_path = packs_dir / name
        self._pack_path.mkdir()
        self.path = str(self._pack_path)

        # Create repo structure
        self._integrations_path = self._pack_path / 'Integrations'
        self._integrations_path.mkdir()

        self._scripts_path = self._pack_path / 'Scripts'
        self._scripts_path.mkdir()

        self._playbooks_path = self._pack_path / 'Playbooks'
        self._playbooks_path.mkdir()

        self._classifiers_path = self._pack_path / 'Classifiers'
        self._classifiers_path.mkdir()

        self._mappers_path = self._classifiers_path

        self._dashboards_path = self._pack_path / 'Dashboards'
        self._dashboards_path.mkdir()

        self._incidents_field_path = self._pack_path / 'IncidentFields'
        self._incidents_field_path.mkdir()

        self._incident_types_path = self._pack_path / 'IncidentTypes'
        self._incident_types_path.mkdir()

        self._indicator_fields = self._pack_path / 'IndicatorFields'
        self._indicator_fields.mkdir()

        self._release_notes = self._pack_path / 'ReleaseNotes'
        self._release_notes.mkdir()

        self.secrets = Secrets(self._pack_path)

        self.pack_ignore = TextBased(self._pack_path, '.pack-ignore')

        self.readme = TextBased(self._pack_path, 'README.md')

        self.pack_metadata = JSONBased(self._pack_path, 'pack_metadata.json', '')

    def create_integration(
            self,
            name: Optional[str] = None,
            code: Optional[str] = None,
            yml: Optional[dict] = None,
            readme: Optional[str] = None,
            description: Optional[str] = None,
            changelog: Optional[str] = None,
            image: Optional[bytes] = None
    ) -> Integration:
        if name is None:
            name = f'integration_{len(self.integrations)}'
        if yml is None:
            yml = {}
        integration = Integration(self._integrations_path, name, self._repo)
        integration.build(
            code,
            yml,
            readme,
            description,
            changelog,
            image
        )
        self.integrations.append(integration)
        return integration

    def create_script(
            self,
            name: Optional[str] = None,
            yml: Optional[dict] = None,
            code: str = '',
            readme: str = '',
            description: str = '',
            changelog: str = '',
            image: bytes = b'') -> Script:
        if name is None:
            name = f'script{len(self.integrations)}'
        if yml is None:
            yml = {}
        script = Script(self._scripts_path, name, self._repo)
        script.build(
            code,
            yml,
            readme,
            description,
            changelog,
            image
        )
        self.scripts.append(script)
        return script

    def create_test_script(self) -> Script:
        script = self.create_script('sample_script')
        script.create_default_script()
        return script

    def _create_json_based(
            self,
            name,
            prefix: str,
            content: dict = None,
            dir_path: Path = None
    ) -> JSONBased:
        if content is None:
            content = {}
        if dir_path:
            obj = JSONBased(dir_path, name, prefix)
        else:
            obj = JSONBased(self._pack_path, name, prefix)
        obj.write_json(content)
        return obj

    def _create_text_based(
            self,
            name,
            content: str = '',
            dir_path: Path = None
    ) -> TextBased:
        if dir_path:
            obj = TextBased(dir_path, name)
        else:
            obj = TextBased(self._pack_path, name)
        obj.write_text(content)
        return obj

    def create_classifier(
            self,
            name,
            content: dict = None
    ) -> JSONBased:
        prefix = 'classifier'
        classifier = self._create_json_based(name, prefix, content, dir_path=self._classifiers_path)
        self.classifiers.append(classifier)
        return classifier

    def create_mapper(
            self,
            name,
            content: dict = None
    ) -> JSONBased:
        prefix = 'classifier-mapper'
        mapper = self._create_json_based(name, prefix, content)
        self.mapper.append(mapper)
        return mapper

    def create_dashboard(
            self,
            name,
            content: dict = None
    ) -> JSONBased:
        prefix = 'dashboard'
        dashboard = self._create_json_based(name, prefix, content)
        self.dashboards.append(dashboard)
        return dashboard

    def create_incident_field(
            self,
            name,
            content: dict = None,
            release_notes: bool = False
    ) -> JSONBased:
        prefix = 'incidentfield'
        incident_field = self._create_json_based(name, prefix, content)
        if release_notes:
            release_notes = self._create_text_based(f'{incident_field}_CHANGELOG.md',
                                                    dir_path=self._incidents_field_path)
            self.incident_field.append(release_notes)
        self.incident_field.append(incident_field)
        return incident_field

    def create_incident_type(
            self,
            name,
            content: dict = None) -> JSONBased:
        prefix = 'incidenttype'
        incident_type = self._create_json_based(name, prefix, content)
        self.incident_types.append(incident_type)
        return incident_type

    def create_indicator_field(
            self,
            name,
            content: dict = None
    ) -> JSONBased:
        prefix = 'incidentfield'
        indicator_field = self._create_json_based(name, prefix, content)
        self.indicator_field.append(indicator_field)
        return indicator_field

    def create_indicator_type(
            self,
            name,
            content: dict = None
    ) -> JSONBased:
        prefix = 'reputation'
        indicator_type = self._create_json_based(name, prefix, content)
        self.indicator_type.append(indicator_type)
        return indicator_type

    def create_layout(
            self,
            name,
            content: dict = None
    ) -> JSONBased:
        prefix = 'layout'
        layout = self._create_json_based(name, prefix, content)
        self.layouts.append(layout)
        return layout

    def create_release_notes(self, version: str, content: str = ''):
        rn = self._create_text_based(f'{version}.md', content, dir_path=self._release_notes)
        self.release_notes.append(rn)
        return rn
