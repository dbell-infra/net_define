from netdefine.src.template import ConfigTemplate
from .data import template_text, feature_text, component_text, bad_feature_text
import pytest


# Set up directory structure and test files for test session
@pytest.fixture()
def file_structure(tmp_path):

    root = tmp_path / 'globomantics'
    root.mkdir()

    features = tmp_path / 'globomantics/features'
    features.mkdir()
    test_feature = features / 'test_feature.yml'
    test_feature.write_text(feature_text)

    templates = tmp_path / 'globomantics/templates'
    templates.mkdir()
    test_template = templates / "test_template.yml"
    test_template.write_text(template_text)

    components = tmp_path / 'globomantics/components'
    components.mkdir()
    test_component = components / "test_component.j2"
    test_component.write_text(component_text)

    configs = tmp_path / 'globomantics/configs'
    configs.mkdir()

    return root


def test_config_template_bad_feature(file_structure):
    bad_feature = file_structure / 'features/test_feature.yml'
    bad_feature.write_text(bad_feature_text)
    config = ConfigTemplate(root=file_structure, template='test_template.yml', environment='local')
    with pytest.raises(Exception):
        config.produce_template()

